from rest_framework import serializers
from .models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = [
            "id",
            "user",
            "title",
            "description",
            "start_time",
            "end_time",
            "is_completed",
            "post",
            "created_at",
            "updated_at",
        ]
