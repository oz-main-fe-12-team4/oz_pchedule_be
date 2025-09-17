from django.db import models
from apps.user.models import User


class Post(models.Model):
    CATEGORY_CHOICES = [
        ("여행", "여행"),
        ("일정", "일정"),
        ("기타", "기타"),
    ]

    PRIORITY_CHOICES = [
        ("긴급", "긴급"),
        ("높음", "높음"),
        ("보통", "보통"),
        ("낮음", "낮음"),
        ("여유", "여유"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)

    start_period = models.DateTimeField(null=True, blank=True)
    end_period = models.DateTimeField(null=True, blank=True)
    is_someday = models.BooleanField(default=False)

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)

    is_shared = models.BooleanField(default=False)
    is_recurrence = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# STO 기능: 좋아요, 북마크, 신고
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)


class PostFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorited_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)


class PostReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reported_posts")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reports")
    reason = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
