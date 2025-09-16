from django.db import models
from apps.user.models import User


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("여행", "여행"),
        ("일", "일"),
        ("기타", "기타"),
    ]
    PRIORITY_CHOICES = [
        ("높음", "높음"),
        ("중간", "중간"),
        ("낮음", "낮음"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    start_period = models.DateTimeField()
    end_period = models.DateTimeField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    is_shared = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
