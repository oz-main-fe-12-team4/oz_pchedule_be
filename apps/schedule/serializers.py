from rest_framework import serializers
from .models import Schedule, DetailSchedule, RecurrenceRule, Weekday
from apps.core.profanity_filter import contains_profanity


# 세부 일정 Serializer
class DetailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSchedule
        fields = ["id", "title", "description", "start_time", "end_time", "is_completed"]


# 반복 규칙 Serializer
class RecurrenceRuleSerializer(serializers.ModelSerializer):
    weekdays = serializers.PrimaryKeyRelatedField(many=True, queryset=Weekday.objects.all())
    recurrence_type = serializers.ChoiceField(choices=RecurrenceRule.RECURRENCE_TYPE_CHOICES)

    class Meta:
        model = RecurrenceRule
        fields = ["id", "recurrence_type", "weekdays", "month_of_year", "day_of_month"]

    def validate_month_of_year(self, value):
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("월은 1~12 사이여야 합니다.")
        return value

    def validate_day_of_month(self, value):
        if value and (value < 1 or value > 31):
            raise serializers.ValidationError("일은 1~31 사이여야 합니다.")
        return value


# 메인 일정 Serializer
class ScheduleSerializer(serializers.ModelSerializer):
    detail_schedule = DetailScheduleSerializer(many=True, required=False)
    recurrence_rule = RecurrenceRuleSerializer(required=False)
    category_name = serializers.CharField(source="category.name", read_only=True)

    priority = serializers.ChoiceField(choices=Schedule._meta.get_field("priority").choices)
    share_type = serializers.ChoiceField(choices=Schedule._meta.get_field("share_type").choices)

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
            "is_completed",
            "detail_schedule",
            "recurrence_rule",
        ]

    def validate(self, attrs):
        is_someday = attrs.get("is_someday", False)
        start_period = attrs.get("start_period")
        end_period = attrs.get("end_period")

        if not is_someday and (not start_period or not end_period):
            raise serializers.ValidationError("시작일과 종료일은 필수입니다 (is_someday=False)")

        if start_period and end_period and end_period < start_period:
            raise serializers.ValidationError("종료일은 시작일보다 이후여야 합니다.")

        return attrs

    def create(self, validated_data):
        details = validated_data.pop("detail_schedule", [])
        recurrence_data = validated_data.pop("recurrence_rule", None)

        print(validated_data)
        schedule = Schedule.objects.create(**validated_data)

        for d in details:
            DetailSchedule.objects.create(schedule=schedule, **d)

        if recurrence_data:
            weekdays = recurrence_data.pop("weekdays", [])
            rule = RecurrenceRule.objects.create(schedule=schedule, **recurrence_data)
            rule.weekdays.set(weekdays)

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
            weekdays = recurrence_data.pop("weekdays", [])
            if hasattr(instance, "recurrence_rule"):
                for attr, value in recurrence_data.items():
                    setattr(instance.recurrence_rule, attr, value)
                instance.recurrence_rule.save()
                instance.recurrence_rule.weekdays.set(weekdays)
            else:
                rule = RecurrenceRule.objects.create(schedule=instance, **recurrence_data)
                rule.weekdays.set(weekdays)

        return instance

    def validate_title(self, value):
        if contains_profanity(value):
            raise serializers.ValidationError("부적절한 단어가 포함되어 있습니다.")
        return value
