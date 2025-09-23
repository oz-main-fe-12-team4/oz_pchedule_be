from rest_framework import serializers
from .models import Category, Schedule, DetailSchedule, Recurrence, Weekday


# --- Category ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]  # 생성 시 id는 서버에서 자동 할당


# --- Weekday ---
class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ["id"]  # read-only만 허용
        read_only_fields = ["id"]


# --- Recurrence ---
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
            "created_at",
        ]
        read_only_fields = ["id", "weekdays", "created_at"]


# --- DetailSchedule ---
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
        read_only_fields = [
            "id",
            "is_completed",  # 서버 complete 액션에서만 변경
            "completed_at",  # 서버에서 자동 기록
            "created_at",
            "updated_at",
        ]


# --- Schedule ---
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
        read_only_fields = [
            "id",
            "like_count",  # 좋아요, 북마크 서버 처리
            "bookmark_count",
            "created_at",
            "updated_at",
            "recurrences",
            "details",
        ]
