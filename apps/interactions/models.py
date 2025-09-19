from django.db import models
from apps.user.models import User
from apps.post.models import Post


class Like(models.Model):
    like_id = models.CompositePrimaryKey("user", "post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "like"

    def __str__(self):
        return f"like ID = {self.like_id}"


class Bookmark(models.Model):
    bookmark_id = models.CompositePrimaryKey("user", "post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmark"

    def __str__(self):
        return f"bookmark ID = {self.bookmark_id}"


class Report(models.Model):
    report_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"report ID = {self.report_id}"
