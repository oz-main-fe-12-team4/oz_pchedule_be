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

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


# 일정 테이블
class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="중간")
    share_type = models.CharField(max_length=10, choices=SHARE_CHOICES, default="비공개")
    is_someday = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "schedule"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


# 요일 테이블
class Weekday(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=10)

    class Meta:
        db_table = "weekday"

    def __str__(self):
        return self.name


# 반복 규칙 테이블
class RecurrenceRule(models.Model):
    FREQUENCY_CHOICES = [
        ("DAILY", "Daily"),
        ("WEEKLY", "Weekly"),
        ("MONTHLY", "Monthly"),
        ("YEARLY", "Yearly"),
    ]

    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name="recurrence_rule")
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    interval = models.PositiveIntegerField(default=1)
    weekdays = models.ManyToManyField(Weekday, blank=True)
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
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "detail_schedule"

    def __str__(self):
        return f"{self.title} - {self.schedule.title}"
