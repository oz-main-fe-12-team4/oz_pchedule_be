from django.db import models
from apps.user.models import User

PRIORITY_CHOICES = [
    ("긴급", "긴급"),
    ("높음", "높음"),
    ("중간", "중간"),
    ("낮음", "낮음"),
    ("보류", "보류"),
]

SHARE_CHOICES = [
    ("비공개", "비공개"),
    ("친구공개", "친구공개"),
    ("전체공개", "전체공개"),
]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.name


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="중간", null=False)
    share_type = models.CharField(max_length=10, choices=SHARE_CHOICES, default="비공개")
    is_someday = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)
    recurrence_type = models.CharField(max_length=10, blank=True, null=True)  # daily, weekly, monthly, yearly
    recurrence_weekdays = models.JSONField(blank=True, null=True)  # ["월", "화"]
    recurrence_day_of_month = models.IntegerField(blank=True, null=True)
    recurrence_month_of_year = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "schedule"

    def __str__(self):
        return f"{self.title} ({self.user.username})"


class DetailSchedule(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="detail_schedule")
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "detail_schedule"

    def __str__(self):
        return f"{self.title} - {self.schedule.title}"
