from django.db import models
from apps.user.models import User


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("일상", "일상"),
        ("취미/여가", "취미/여가"),
        ("여행", "여행"),
        ("자기 계발/학습", "자기 계발/학습"),
        ("이벤트", "이벤트"),
        ("기타", "기타"),
    ]

    PRIORITY_CHOICES = [
        ("긴급", "긴급"),
        ("높음", "높음"),
        ("중간", "중간"),
        ("낮음", "낮음"),
        ("보류", "보류"),
    ]

    SHARE_CHOICES = [
        ("private", "비공개"),
        ("public", "전체 공개"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=50)
    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="중간")
    share_type = models.CharField(max_length=20, choices=SHARE_CHOICES, default="private")
    is_recurrence = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
