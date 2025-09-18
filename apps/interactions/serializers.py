from rest_framework import serializers
from .models import Like, Favorite, Report


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = []

    def create(self, validated_data):
        user = self.context["request"].user
        post = self.context["post"]
        return Report.objects.create(user=user, post=post, **validated_data)


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = []

    def create(self, validated_data):
        user = self.context["request"].user
        post = self.context["post"]
        return Favorite.objects.create(user=user, post=post, **validated_data)


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["reason"]

    def create(self, validated_data):
        user = self.context["request"].user
        post = self.context["post"]
        return Report.objects.create(user=user, post=post, **validated_data)
