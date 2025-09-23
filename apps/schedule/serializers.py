from rest_framework import serializers
from .models import Category, Schedule, DetailSchedule, Recurrence, Weekday


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ["id"]


class RecurrenceSerializer(serializers.ModelSerializer):
    weekdays = WeekdaySerializer(many=True, read_only=True)
    weekday_ids = serializers.PrimaryKeyRelatedField(
        queryset=Weekday.objects.all(), many=True, write_only=True, source="weekdays"
    )

    class Meta:
        model = Recurrence
        fields = [
            "id",
            "type",
            "weekdays",
            "weekday_ids",
            "day_of_month",
            "month_of_year",
            "count",
            "until",
        ]


class DetailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSchedule
        fields = [
            "id",
            "schedule",
            "title",
            "description",
            "start_time",
            "end_time",
            "alert_minute",
            "is_completed",
            "completed_at",
            "created_at",
            "updated_at",
        ]


class ScheduleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    recurrences = RecurrenceSerializer(many=True, read_only=True)
    details = DetailScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = [
            "id",
            "user",
            "title",
            "category",
            "category_id",
            "priority",
            "share_type",
            "is_recurrence",
            "start_period",
            "end_period",
            "like_count",
            "bookmark_count",
            "created_at",
            "updated_at",
            "recurrences",
            "details",
        ]
        read_only_fields = ["like_count", "bookmark_count", "created_at", "updated_at"]
