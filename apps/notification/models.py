from django.db import models
from apps.user.models import User


class Notification(models.Model):
    NOTIFICATION_TYPES = [("like", "Like"), ("bookmark", "Bookmark"), ("report", "Report"), ("schedule", "Schedule")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    content = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"Notification ID = {self.id}, User ID = {self.user.id}"
