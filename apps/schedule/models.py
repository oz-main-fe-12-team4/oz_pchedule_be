from django.db import models
from apps.user.models import User
from apps.post.models import Post


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedules")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Recurrence(models.Model):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="recurrences")
    RECURRENCE_TYPE = [
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]
    recurrence_type = models.CharField(max_length=10, choices=RECURRENCE_TYPE)
    interval = models.PositiveIntegerField(default=1)  # 매 1일, 매 2주 등
    end_date = models.DateTimeField(null=True, blank=True)
