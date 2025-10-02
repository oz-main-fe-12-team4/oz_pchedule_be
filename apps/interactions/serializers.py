from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reason = serializers.ChoiceField(choices=Report.REASONS)

    class Meta:
        model = Report
        fields = ["id", "reason", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        schedule = self.context["schedule"]
        return Report.objects.create(user=user, schedule=schedule, **validated_data)
