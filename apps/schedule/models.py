from django.db import models
from django.conf import settings
from apps.post.models import Post
from django.utils import timezone


class Schedule(models.Model):
    RECUR_RULE_CHOICES = [
        ("daily", "매일"),
        ("weekly", "매주"),
        ("monthly", "매월"),
        ("yearly", "매년"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schedules")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="schedules", null=True, blank=True)

    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    alert_minute = models.PositiveIntegerField(default=0)

    # 완료 처리
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    # 반복 설정
    recur_rule = models.CharField(max_length=10, choices=RECUR_RULE_CHOICES, blank=True, null=True)
    recur_interval = models.PositiveIntegerField(default=1)  # 반복 주기
    recur_count = models.PositiveIntegerField(null=True, blank=True)  # 반복 횟수
    recur_until = models.DateField(null=True, blank=True)  # 반복 종료일

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_completed(self):
        """일정 완료 처리 메서드"""
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.title} ({self.start_time} ~ {self.end_time})"
