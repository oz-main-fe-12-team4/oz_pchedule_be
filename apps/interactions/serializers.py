from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    reason = serializers.ChoiceField(choices=Report.REASONS)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Report
        fields = ["id", "reason", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        schedule = self.context["schedule"]
        return Report.objects.create(user=user, schedule=schedule, **validated_data)
