from rest_framework import serializers


class ReportSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=50)
