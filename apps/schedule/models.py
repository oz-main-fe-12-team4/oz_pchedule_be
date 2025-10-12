from django.db import models
from apps.user.models import User

# 우선순위 선택지
PRIORITY_CHOICES = [
    ("긴급", "긴급"),
    ("높음", "높음"),
    ("중간", "중간"),
    ("낮음", "낮음"),
    ("보류", "보류"),
]

# 공유 범위 선택지
SHARE_CHOICES = [
    ("비공개", "비공개"),
    ("전체공개", "전체공개"),
]


# 카테고리 테이블
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


# 메인 일정 테이블
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="중간")
    share_type = models.CharField(max_length=10, choices=SHARE_CHOICES, default="비공개")
    is_someday = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)  # 반복 여부
    is_reported = models.BooleanField(default=False)  # 신고 여부

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedule"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


# 요일 테이블
class Weekday(models.Model):
    WEEKDAY_CHOICES = [
        ("SU", "일"),
        ("MO", "월"),
        ("TU", "화"),
        ("WE", "수"),
        ("TH", "목"),
        ("FR", "금"),
        ("SA", "토"),
    ]

    code = models.CharField(max_length=2, unique=True, choices=WEEKDAY_CHOICES)
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "weekday"

    def __str__(self):
        return self.name


# 반복 규칙 테이블
class RecurrenceRule(models.Model):
    RECURRENCE_TYPE_CHOICES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name="recurrence_rule")
    recurrence_type = models.CharField(
        max_length=10, choices=RECURRENCE_TYPE_CHOICES, null=True, blank=True
    )  # 반복 타입
    weekdays = models.ManyToManyField(Weekday, blank=True)  # 요일 선택
    month_of_year = models.PositiveIntegerField(null=True, blank=True)
    day_of_month = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = "recurrence_rule"


# 세부 일정 테이블
class DetailSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="detail_schedule")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)  # 개별 일정 완료 여부
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "detail_schedule"

    def __str__(self):
        return f"{self.title} - {self.schedule.title}"
