from django.db import models
from apps.user.models import User
from apps.schedule.models import Schedule


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        db_table = "like"
        constraints = [models.UniqueConstraint(fields=["user", "schedule"], name="unique_user_schedule")]

    def __str__(self):
        return f"Like(id={self.id}, user={self.user_id}, schedule={self.schedule_id})"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    class Meta:
        db_table = "bookmark"
        constraints = [models.UniqueConstraint(fields=["user", "schedule"], name="unique_user_schedule_bookmark")]

    def __str__(self):
        return f"Bookmark(id={self.id}, user={self.user_id}, schedule={self.schedule_id})"


class Report(models.Model):
    REASONS = [
        ("NAME", "부적절한 이름"),
        ("CONTENT", "부적절한 내용"),
        ("SPAM", "도배"),
        ("ABUSE", "욕설"),
        ("SEXUAL", "선정적인 내용"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, null=False, choices=REASONS)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "report"

    def __str__(self):
        return f"report ID = {self.report_id}"
