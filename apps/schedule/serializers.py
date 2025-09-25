from rest_framework import serializers
from .models import Schedule, DetailSchedule


class DetailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSchedule
        fields = ["id", "title", "description", "start_time", "end_time", "is_completed"]


class ScheduleSerializer(serializers.ModelSerializer):
    detail_schedule = DetailScheduleSerializer(many=True, required=False)
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = Schedule
        fields = [
            "id",
            "title",
            "start_period",
            "end_period",
            "category",
            "category_name",
            "priority",
            "share_type",
            "is_recurrence",
            "recurrence_type",
            "recurrence_weekdays",
            "recurrence_day_of_month",
            "recurrence_month_of_year",
            "is_someday",
            "detail_schedule",
        ]

    def create(self, validated_data):
        details = validated_data.pop("detail_schedule", [])
        schedule = Schedule.objects.create(**validated_data)
        for d in details:
            DetailSchedule.objects.create(schedule=schedule, **d)
        return schedule

    def update(self, instance, validated_data):
        details = validated_data.pop("detail_schedule", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if details is not None:
            instance.detail_schedule.all().delete()
            for d in details:
                DetailSchedule.objects.create(schedule=instance, **d)
        return instance
