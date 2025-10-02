from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    # 👇 request.user 자동으로 채워줌
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    reason = serializers.ChoiceField(choices=Report.REASONS)

    class Meta:
        model = Report
        fields = ["id", "reason", "created_at"]
        read_only_fields = ["id", "created_at"]
