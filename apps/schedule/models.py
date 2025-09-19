from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError


class Category(models.Model):
    """사용자가 선택할 수 있는 일정 카테고리"""

    CATEGORY_CHOICES = [
        ("일상", "🏠 일상"),
        ("취미/여가", "🎨 취미/여가"),
        ("여행", "✈️ 여행"),
        ("자기계발/학습", "📚 자기계발/학습"),
        ("특별이벤트", "🎉 특별이벤트"),
        ("기타", "🌀 기타"),
    ]

    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Schedule(models.Model):
    """일정 묶음 / 일정 메인"""

    PRIORITY_CHOICES = [
        ("긴급", "긴급"),
        ("높음", "높음"),
        ("중간", "중간"),
        ("낮음", "낮음"),
        ("보류", "보류"),
    ]

    SHARE_CHOICES = [
        ("전체공개", "전체공개"),
        ("나만보기", "나만보기"),
    ]

    schedule_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedules")
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="schedules")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="중간")
    share_type = models.CharField(max_length=20, choices=SHARE_CHOICES, default="나만보기")
    is_recurrence = models.BooleanField(default=False)

    start_period = models.DateTimeField()
    end_period = models.DateTimeField()

    like_count = models.PositiveIntegerField(default=0)
    bookmark_count = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시 자동 기록
    updated_at = models.DateTimeField(auto_now=True)  # 수정 시 자동 기록

    class Meta:
        indexes = [models.Index(fields=["user", "created_at"])]
        ordering = [
            models.Case(
                models.When(priority="긴급", then=0),
                models.When(priority="높음", then=1),
                models.When(priority="중간", then=2),
                models.When(priority="낮음", then=3),
                models.When(priority="보류", then=4),
                output_field=models.IntegerField(),
            )
        ]

    def clean(self):
        if self.end_period < self.start_period:
            raise ValidationError({"end_period": "end_period must be after or equal to start_period."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.user})"


class DetailSchedule(models.Model):
    """일정 안의 상세 일정"""

    detail_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="details")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    alert_minute = models.PositiveIntegerField(default=0)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["schedule", "start_time", "end_time"])]

    def clean(self):
        if self.end_time < self.start_time:
            raise ValidationError({"end_time": "end_time must be after or equal to start_time."})
        if self.schedule:
            if (
                self.start_time.date() < self.schedule.start_period.date()
                or self.end_time.date() > self.schedule.end_period.date()
            ):
                raise ValidationError("Detail schedule must be within parent schedule period.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.schedule.title})"


class Weekday(models.Model):
    """요일 (반복 규칙 ManyToMany용)"""

    DAYS = [
        (0, "월"),
        (1, "화"),
        (2, "수"),
        (3, "목"),
        (4, "금"),
        (5, "토"),
        (6, "일"),
    ]

    id = models.PositiveSmallIntegerField(choices=DAYS, primary_key=True)

    def __str__(self):
        return dict(self.DAYS).get(self.id, str(self.id))


class Recurrence(models.Model):
    """반복 일정 규칙"""

    TYPE_CHOICES = [
        ("Daily", "매일"),
        ("Weekly", "매주"),
        ("Monthly", "매월"),
        ("Yearly", "매년"),
    ]

    recurrence_id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="recurrences")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    interval = models.PositiveIntegerField(default=1)

    # ManyToMany: 여러 요일 선택 가능
    weekdays = models.ManyToManyField(Weekday, blank=True, related_name="recurrences")

    day_of_month = models.PositiveSmallIntegerField(blank=True, null=True)
    month_of_year = models.PositiveSmallIntegerField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    count = models.PositiveIntegerField(blank=True, null=True)
    until = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.type == "Weekly" and not self.weekdays.exists():
            raise ValidationError("Weekly recurrence requires at least one weekday.")
        if self.type == "Monthly" and not (self.day_of_month or self.weekdays.exists()):
            raise ValidationError("Monthly recurrence should specify day_of_month or weekdays.")

    def __str__(self):
        return f"{self.schedule.title} - {self.type} every {self.interval}"
