from django.db import models


class Notification(models.Model):
    notification_id = models.AutoField(primary_key=True, auto_created=True)
    user_id = models.ForeignKey("user.User", on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification"

    def __str__(self):
        return f"Notification ID = {self.notification_id}, User ID = {self.user_id}, Message = {self.message}"
