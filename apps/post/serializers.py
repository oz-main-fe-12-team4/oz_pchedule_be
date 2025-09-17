from rest_framework import serializers
from .models import Post
from apps.schedule.models import Schedule, Recurrence


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"
        read_only_fields = ["post", "created_at", "updated_at"]


class RecurrenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recurrence
        fields = "__all__"
        read_only_fields = ["post"]


class PostSerializer(serializers.ModelSerializer):
    schedules = ScheduleSerializer(many=True, read_only=True)
    recurrences = RecurrenceSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["user", "created_at", "updated_at"]
