from django.db import models
from apps.user.models import User


class Post(models.Model):
    class Category(models.TextChoices):
        DAILY = "일상", "일상"
        HOBBY = "취미/여가", "취미/여가"
        TRAVEL = "여행", "여행"
        SELF_DEV = "자기계발/학습", "자기계발/학습"
        EVENT = "이벤트", "이벤트"
        ETC = "기타", "기타"

    class Priority(models.TextChoices):
        URGENT = "긴급", "긴급"
        HIGH = "높음", "높음"
        MEDIUM = "보통", "보통"
        LOW = "낮음", "낮음"
        RELAXED = "보류", "보류"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    is_someday = models.BooleanField(default=False)

    category = models.CharField(max_length=20, choices=Category.choices)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)

    is_shared = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.category}] {self.title}"
