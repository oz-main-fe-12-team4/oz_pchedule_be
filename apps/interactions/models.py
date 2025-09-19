from django.db import models
from apps.user.models import User
from apps.post.models import Post


class Like(models.Model):
    like_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "like"

    def __str__(self):
        return f"like ID = {self.like_id}"


class Favorite(models.Model):
    favorite_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "favorite"

    def __str__(self):
        return f"favorite ID = {self.favorite_id}"


class Report(models.Model):
    REASON = [
        ("Inappropriate name", "부적절한 이름"),
        ("Inappropriate content", "부적절한 내용"),
        ("Spamming", "도배"),
        ("Profanity", "욕설"),
        ("Sexually explicit content", "선정적인 내용"),
    ]

    report_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=REASON)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"report ID = {self.report_id}"
