from django.db import models
from apps.user.models import User


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, null=False)
    content = models.CharField(max_length=50, null=False)
    is_read = models.BooleanField(default=False, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=False)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"Notification ID = {self.notification_id}, User ID = {self.user_id}"
