from django.db import models
from django.conf import settings


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("여행", "여행"),
        ("업무", "업무"),
        ("공부", "공부"),
        ("자기계발", "자기계발"),
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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")

    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=10, default="중간")
    is_shared = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.category}/{self.priority}] {self.title}"
