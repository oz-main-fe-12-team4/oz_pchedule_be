from django.db import models
from apps.user.models import User
from apps.schedule.models import Schedule


class Like(models.Model):
    like_id = models.CompositePrimaryKey("user", "schedule")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        db_table = "like"

    def __str__(self):
        return f"like ID = {self.like_id}"


class Bookmark(models.Model):
    bookmark_id = models.CompositePrimaryKey("user", "schedule")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmark"

    def __str__(self):
        return f"bookmark ID = {self.bookmark_id}"


class Report(models.Model):
    REASONS = [
        ("NAME", "부적절한 이름"),
        ("CONTENT", "부적절한 내용"),
        ("SPAM", "도배"),
        ("ABUSE", "욕설"),
        ("SEXUAL", "선정적인 내용"),
    ]

    report_id = models.IntegerField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, null=False, choices=REASONS)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"report ID = {self.report_id}"
