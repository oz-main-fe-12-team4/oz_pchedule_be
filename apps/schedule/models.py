from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone


class Category(models.Model):
    """우선순위/상태 테이블 — 초기값으로 ('긴급','높음','중간','낮음','보류') 를 넣어둡니다."""

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    """일정 (일정 묶음 / Post 개념)"""

    schedule_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedules")
    title = models.CharField(max_length=100)
    # 명세에 따르면 DATETIME (일정 시작/종료일시)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="schedules")
    SHARE_CHOICES = [
        ("전체공개", "전체공개"),
        ("나만보기", "나만보기"),
    ]
    share_type = models.CharField(max_length=20, choices=SHARE_CHOICES, default="나만보기")
    is_recurrence = models.BooleanField(default=False)

    # 캐시용 카운트(별도 Like/Bookmark 모델에서 유지보수)
    like_count = models.PositiveIntegerField(default=0)
    favorite_count = models.PositiveIntegerField(default=0)
    report_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
        ]

    def clean(self):
        # start <= end 검증
        if self.end_period < self.start_period:
            raise ValidationError({"end_period": "end_period must be after or equal to start_period."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.user})"


class DetailSchedule(models.Model):
    """세부 일정(한 Schedule에 여러개)"""

    detail_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    # 상세는 정확한 시각을 가짐
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    alert_minute = models.IntegerField(default=0)  # 명세에 NOT NULL 이었음 -> default 0
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["schedule", "start_time", "end_time"])]

    def clean(self):
        # 시간 순서 검증
        if self.end_time < self.start_time:
            raise ValidationError({"end_time": "end_time must be after or equal to start_time."})
        # detail이 속한 schedule 기간 내에 있는지(옵션)
        if self.schedule:
            if (
                self.start_time.date() < self.schedule.start_period.date()
                or self.end_time.date() > self.schedule.end_period.date()
            ):
                # 허용할 수도 있지만 경고/검증으로 막는 편이 안전
                raise ValidationError("detail start/end must be within parent schedule period.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @transaction.atomic
    def mark_completed(self, user):
        """완료 처리: ScheduleCompletion 생성 + 필드 갱신"""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = timezone.now()
            self.save(update_fields=["is_completed", "completed_at", "updated_at"])
            # ScheduleCompletion 기록 (중복 방지 unique constraint)
            ScheduleCompletion.objects.create(detail_schedule=self, user=user)

    def __str__(self):
        return f"{self.title} ({self.schedule.title})"


class Recurrence(models.Model):
    """반복 규칙"""

    recurrence_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="recurrences")

    TYPE_CHOICES = [
        ("Daily", "Daily"),
        ("Weekly", "Weekly"),
        ("Monthly", "Monthly"),
        ("Yearly", "Yearly"),
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    interval = models.PositiveIntegerField(default=1)  # 매 n 일/주/월/년
    # 요일(월~일) 여러 선택을 지원 -> JSONField로 [0..6] 또는 ["월","수"]
    day_of_week = models.JSONField(blank=True, null=True)  # ex: ["월","수"] 또는 [0,2]
    day_of_month = models.PositiveSmallIntegerField(blank=True, null=True)
    month_of_year = models.PositiveSmallIntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    # 반복 종료 옵션
    count = models.PositiveIntegerField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # 타입에 따라 필요한 필드 존재 검사
        if self.type == "Weekly" and not self.day_of_week:
            raise ValidationError("Weekly recurrence requires day_of_week.")
        if self.type == "Monthly" and not (self.day_of_month or self.day_of_week):
            raise ValidationError("Monthly recurrence should specify day_of_month or day_of_week.")
        # 추가 유효성은 필요에 따라 확장

    def __str__(self):
        return f"{self.schedule.title} - {self.type} (every {self.interval})"


class ScheduleCompletion(models.Model):
    """누가 어떤 detail 일정을 완료했는지 기록 (공유일정에서 필요)"""

    completion_id = models.AutoField(primary_key=True)
    detail_schedule = models.ForeignKey(DetailSchedule, on_delete=models.CASCADE, related_name="completions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedule_completions")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("detail_schedule", "user")
        indexes = [models.Index(fields=["user", "completed_at"])]

    def __str__(self):
        return f"{self.user} completed {self.detail_schedule} at {self.completed_at}"
