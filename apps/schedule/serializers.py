from rest_framework import serializers
from .models import Schedule, DetailSchedule, RecurrenceRule, Weekday
from apps.core.profanity_filter import contains_profanity


# ----------------------
# DetailSchedule Serializer
# ----------------------
class DetailScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailSchedule
        fields = ["id", "title", "description", "start_time", "end_time", "is_completed"]

    def validate(self, attrs):
        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")
        if start_time and end_time and end_time < start_time:
            raise serializers.ValidationError("세부 일정의 종료 시간은 시작 시간보다 이후여야 합니다.")
        return attrs

    def validate_title(self, value):
        if contains_profanity(value):
            raise serializers.ValidationError("부적절한 단어가 포함되어 있습니다.")
        return value

    def validate_description(self, value):
        if contains_profanity(value):
            raise serializers.ValidationError("부적절한 단어가 포함되어 있습니다.")
        return value


# ----------------------
# Weekday Serializer
# ----------------------
class WeekdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Weekday
        fields = ["id", "code", "name"]


# ----------------------
# RecurrenceRule Serializer
# ----------------------
class RecurrenceRuleSerializer(serializers.ModelSerializer):
    WEEKDAYS_CHOICES = [
        ("일", "일"),
        ("월", "월"),
        ("화", "화"),
        ("수", "수"),
        ("목", "목"),
        ("금", "금"),
        ("토", "토"),
    ]

    # GET: Weekday 객체
    weekdays = WeekdaySerializer(many=True, read_only=True)
    # POST/PUT: 이름 리스트
    weekdays_input = serializers.ListField(
        child=serializers.ChoiceField(choices=[name for code, name in WEEKDAYS_CHOICES]),
        write_only=True,
        required=False,
        allow_empty=True,
        default=list,
    )

    recurrence_type = serializers.ChoiceField(
        choices=RecurrenceRule.RECURRENCE_TYPE_CHOICES, allow_null=True, required=False
    )

    class Meta:
        model = RecurrenceRule
        fields = ["id", "recurrence_type", "weekdays", "weekdays_input", "month_of_year", "day_of_month"]

    def create(self, validated_data):
        weekdays_input = validated_data.pop("weekdays_input", [])
        rule = RecurrenceRule.objects.create(**validated_data)
        if weekdays_input:
            code_map = {name: code for code, name in self.WEEKDAYS_CHOICES}
            valid_codes = [code_map[w] for w in weekdays_input if w in code_map]
            weekdays_objs = Weekday.objects.filter(code__in=valid_codes)
            rule.weekdays.set(weekdays_objs)
        return rule

    def update(self, instance, validated_data):
        weekdays_input = validated_data.pop("weekdays_input", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if weekdays_input is not None:
            code_map = {name: code for code, name in self.WEEKDAYS_CHOICES}
            valid_codes = [code_map[w] for w in weekdays_input if w in code_map]
            weekdays_objs = Weekday.objects.filter(code__in=valid_codes)
            instance.weekdays.set(weekdays_objs)
        return instance


# ----------------------
# Schedule Serializer
# ----------------------
class ScheduleSerializer(serializers.ModelSerializer):
    detail_schedule = DetailScheduleSerializer(many=True, required=False)
    recurrence_rule = RecurrenceRuleSerializer(required=False, allow_null=True, default=None)
    category_code = serializers.CharField(source="category.code", read_only=True)
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
            "category_code",
            "priority",
            "share_type",
            "is_someday",
            "is_recurrence",
            "is_reported",
            "detail_schedule",
            "recurrence_rule",
        ]

    def to_representation(self, instance):
        """GET 시 write_only 필드를 완전히 제외"""
        ret = super().to_representation(instance)
        ret.pop("weekdays_input", None)
        return ret

    def validate(self, attrs):
        is_someday = attrs.get("is_someday", False)
        start_period = attrs.get("start_period")
        end_period = attrs.get("end_period")
        if not is_someday and (not start_period or not end_period):
            raise serializers.ValidationError("시작일과 종료일은 필수입니다 (is_someday=False)")
        if start_period and end_period and end_period <= start_period:
            raise serializers.ValidationError("종료일은 시작일보다 이후여야 합니다.")
        return attrs

    def create(self, validated_data):
        details = validated_data.pop("detail_schedule", [])
        recurrence_data = validated_data.pop("recurrence_rule", None)

        schedule = Schedule.objects.create(**validated_data)

        for d in details:
            if isinstance(d, dict):
                DetailSchedule.objects.create(schedule=schedule, **d)

        if recurrence_data:
            weekdays_input = recurrence_data.pop("weekdays_input", [])
            if any(recurrence_data.values()) or weekdays_input:
                code_map = {name: code for code, name in RecurrenceRuleSerializer.WEEKDAYS_CHOICES}
                rule = RecurrenceRule.objects.create(schedule=schedule, **recurrence_data)
                weekdays_objs = Weekday.objects.filter(code__in=[code_map[w] for w in weekdays_input])
                rule.weekdays.set(weekdays_objs)

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
                if isinstance(d, dict):
                    DetailSchedule.objects.create(schedule=instance, **d)

        if recurrence_data is not None:
            weekdays_input = recurrence_data.pop("weekdays_input", [])
            if hasattr(instance, "recurrence_rule") and instance.recurrence_rule:
                for attr, value in recurrence_data.items():
                    setattr(instance.recurrence_rule, attr, value)
                instance.recurrence_rule.save()
                code_map = {name: code for code, name in RecurrenceRuleSerializer.WEEKDAYS_CHOICES}
                weekdays_objs = Weekday.objects.filter(code__in=[code_map[w] for w in weekdays_input])
                instance.recurrence_rule.weekdays.set(weekdays_objs)
            else:
                if any(recurrence_data.values()) or weekdays_input:
                    code_map = {name: code for code, name in RecurrenceRuleSerializer.WEEKDAYS_CHOICES}
                    rule = RecurrenceRule.objects.create(schedule=instance, **recurrence_data)
                    weekdays_objs = Weekday.objects.filter(code__in=[code_map[w] for w in weekdays_input])
                    rule.weekdays.set(weekdays_objs)

        return instance

    def validate_title(self, value):
        if contains_profanity(value):
            raise serializers.ValidationError("부적절한 단어가 포함되어 있습니다.")
        return value
