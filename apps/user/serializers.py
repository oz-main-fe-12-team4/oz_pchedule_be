from rest_framework import serializers
from .models import User, LoginAttempt, Token, AccessTokenBlacklist


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "password", "name", "profile_image", "allow_notification", "created_at", "updated_at"]


class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = "__all__"


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


class AccessTokenBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTokenBlacklist
        fields = "__all__"
