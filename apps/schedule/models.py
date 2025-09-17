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

    def __str__(self):
        return self.title


class Recurrence(models.Model):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

    RECURRENCE_TYPE_CHOICES = [
        (DAILY, "Daily"),
        (WEEKLY, "Weekly"),
        (MONTHLY, "Monthly"),
    ]

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE, related_name="recurrences")
    recurrence_type = models.CharField(max_length=10, choices=RECURRENCE_TYPE_CHOICES)
    interval = models.PositiveIntegerField(default=1)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.schedule.title} ({self.recurrence_type})"
