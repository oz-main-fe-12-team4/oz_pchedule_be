from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(read_only=True)
    is_read = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "content", "is_read", "created_at"]
