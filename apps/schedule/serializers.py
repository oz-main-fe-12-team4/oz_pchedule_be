from rest_framework import serializers
from .models import Schedule, DetailSchedule, RecurrenceRule, Weekday
from apps.core.profanity_filter import contains_profanity


# 세부 일정 Serializer
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


# 반복 규칙 Serializer
class RecurrenceRuleSerializer(serializers.ModelSerializer):
    # 사용자에게 보여줄 한글 선택지
    WEEKDAYS_CHOICES = [
        ("MO", "월"),
        ("TU", "화"),
        ("WE", "수"),
        ("TH", "목"),
        ("FR", "금"),
        ("SA", "토"),
        ("SU", "일"),
    ]

    # 사용자 입력: ["월", "화"] 형태
    weekdays = serializers.ListField(
        child=serializers.ChoiceField(choices=[name for code, name in WEEKDAYS_CHOICES]),
        required=False,
        allow_empty=True,
        default=list,  # 빈 리스트일 경우 기본값
        source="weekdays",  # ManyToManyField에서 queryset 가져오기
    )

    recurrence_type = serializers.ChoiceField(
        choices=RecurrenceRule.RECURRENCE_TYPE_CHOICES, allow_null=True, required=False
    )

    class Meta:
        model = RecurrenceRule
        fields = ["id", "recurrence_type", "weekdays", "month_of_year", "day_of_month"]

    # month_of_year 유효성 검사
    def validate_month_of_year(self, value):
        if value and (value < 1 or value > 12):
            raise serializers.ValidationError("월은 1~12 사이여야 합니다.")
        return value

    # day_of_month 유효성 검사
    def validate_day_of_month(self, value):
        if value and (value < 1 or value > 31):
            raise serializers.ValidationError("일은 1~31 사이여야 합니다.")
        return value

    # DB 저장 시 Weekday 객체로 변환
    def create(self, validated_data):
        weekdays_input = validated_data.pop("weekdays", [])
        code_map = {name: code for code, name in self.WEEKDAYS_CHOICES}
        weekdays_objs = Weekday.objects.filter(code__in=[code_map[w] for w in weekdays_input])
        rule = RecurrenceRule.objects.create(**validated_data)
        rule.weekdays.set(weekdays_objs)
        return rule

    # DB 업데이트 시 Weekday 객체로 변환
    def update(self, instance, validated_data):
        weekdays_input = validated_data.pop("weekdays", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if weekdays_input is not None:
            code_map = {name: code for code, name in self.WEEKDAYS_CHOICES}
            weekdays_objs = Weekday.objects.filter(code__in=[code_map[w] for w in weekdays_input])
            instance.weekdays.set(weekdays_objs)

        return instance


# 요일 Serializer
class WeekdaySerializer(serializers.ModelSerializer):
    code = serializers.CharField(read_only=True)

    class Meta:
        model = Weekday
        fields = ["id", "code", "name"]

    # 요청 데이터 처리: name -> code 매핑
    def to_internal_value(self, data):
        if "name" in data and "code" not in data:
            try:
                weekday_obj = Weekday.objects.get(name=data["name"])
                data["code"] = weekday_obj.code
            except Weekday.DoesNotExist:
                raise serializers.ValidationError({"name": f"'{data['name']}'는 올바른 요일이 아닙니다."})
        return super().to_internal_value(data)


# 메인 일정 Serializer
class ScheduleSerializer(serializers.ModelSerializer):
    detail_schedule = DetailScheduleSerializer(many=True, required=False)
    recurrence_rule = RecurrenceRuleSerializer(required=False, allow_null=True)
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
            "is_recurrence",
            "is_reported",
            "detail_schedule",
            "recurrence_rule",
        ]

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
            DetailSchedule.objects.create(schedule=schedule, **d)

        if recurrence_data:
            weekdays = recurrence_data.pop("weekdays", [])
            if any(recurrence_data.values()) or weekdays:  # 값이 있으면만 생성
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
                if any(recurrence_data.values()) or weekdays:  # 값이 있는 경우만 생성
                    rule = RecurrenceRule.objects.create(schedule=instance, **recurrence_data)
                    rule.weekdays.set(weekdays)

        return instance

    def validate_title(self, value):
        if contains_profanity(value):
            raise serializers.ValidationError("부적절한 단어가 포함되어 있습니다.")
        return value
