from rest_framework import serializers
from .models import Schedule, DetailSchedule, RecurrenceRule, Weekday


class DetailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSchedule
        fields = ["id", "title", "description", "start_time", "end_time", "is_completed"]


class RecurrenceRuleSerializer(serializers.ModelSerializer):
    by_day = serializers.PrimaryKeyRelatedField(many=True, queryset=Weekday.objects.all())

    class Meta:
        model = RecurrenceRule
        fields = ["id", "frequency", "interval", "by_day", "by_month", "by_month_day"]

    def validate_by_month(self, value):
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("월은 1~12 사이여야 합니다.")
        return value

    def validate_by_month_day(self, value):
        if value and (value < 1 or value > 31):
            raise serializers.ValidationError("일은 1~31 사이여야 합니다.")
        return value


class ScheduleSerializer(serializers.ModelSerializer):
    detail_schedule = DetailScheduleSerializer(many=True, required=False)
    recurrence_rule = RecurrenceRuleSerializer(required=False)
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
            "is_someday",
            "is_complete",
            "detail_schedule",
            "recurrence_rule",
        ]

    def create(self, validated_data):
        details = validated_data.pop("detail_schedule", [])
        recurrence_data = validated_data.pop("recurrence_rule", None)

        schedule = Schedule.objects.create(**validated_data)

        for d in details:
            DetailSchedule.objects.create(schedule=schedule, **d)

        if recurrence_data:
            by_day = recurrence_data.pop("by_day", [])
            rule = RecurrenceRule.objects.create(schedule=schedule, **recurrence_data)
            rule.by_day.set(by_day)

        return schedule

    def update(self, instance, validated_data):
        details = validated_data.pop("detail_schedule", None)
        recurrence_data = validated_data.pop("recurrence_rule", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details is not None:
            instance.detail_schedule.all().delete()
            for d in details:
                DetailSchedule.objects.create(schedule=instance, **d)

        if recurrence_data is not None:
            by_day = recurrence_data.pop("by_day", [])
            if hasattr(instance, "recurrence_rule"):
                for attr, value in recurrence_data.items():
                    setattr(instance.recurrence_rule, attr, value)
                instance.recurrence_rule.save()
                instance.recurrence_rule.by_day.set(by_day)
            else:
                rule = RecurrenceRule.objects.create(schedule=instance, **recurrence_data)
                rule.by_day.set(by_day)

        return instance
