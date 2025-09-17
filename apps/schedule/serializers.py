from rest_framework import serializers
from .models import Schedule, Recurrence
from apps.post.models import Post


class RecurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurrence
        fields = "__all__"
        read_only_fields = ["post"]  # post는 생성 시 perform_create에서 지정


class ScheduleSerializer(serializers.ModelSerializer):
    recurrences = RecurrenceSerializer(many=True, read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Schedule
        fields = [
            "id",
            "user",
            "post",
            "title",
            "description",
            "start_time",
            "end_time",
            "alert_minute",
            "is_completed",
            "completed_at",
            "recurrences",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["user", "created_at", "updated_at"]
