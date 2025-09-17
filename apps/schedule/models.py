from django.db import models
from apps.post.models import Post


class Schedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="schedules")
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    alert_minute = models.IntegerField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Recurrence(models.Model):
    TYPE_CHOICES = [
        ("daily", "매일"),
        ("weekly", "매주"),
        ("monthly", "매달"),
        ("yearly", "매년"),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="recurrences")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    day_of_week = models.CharField(max_length=10, null=True, blank=True)  # MON, TUE, ...
    day_of_month = models.PositiveSmallIntegerField(null=True, blank=True)
    month_of_year = models.PositiveSmallIntegerField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.post.title} ({self.type})"
