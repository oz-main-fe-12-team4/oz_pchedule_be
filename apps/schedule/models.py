from django.db import models
from apps.post.models import Post


class Schedule(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="schedules")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.start_time} ~ {self.end_time})"


class RecurrenceRule(models.Model):
    schedule = models.OneToOneField(Schedule, on_delete=models.CASCADE, related_name="recurrence")
    frequency = models.CharField(
        max_length=20,
        choices=[
            ("DAILY", "매일"),
            ("WEEKLY", "매주"),
            ("MONTHLY", "매월"),
            ("ANNUALLY", "매년"),
        ],
    )
    interval = models.PositiveIntegerField(default=1)
    count = models.PositiveIntegerField(null=True, blank=True)
    until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.schedule.title} 반복 ({self.frequency})"
