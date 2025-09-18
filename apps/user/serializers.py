from rest_framework import serializers
from .models import User, LoginAttempt, Token, AccessTokenBlacklist


# 회원가입/유저 조회 용
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",  # PK (user_id)
            "email",
            "password",
            "name",
            "profile_image",
            "allow_notification",
            "created_at",
            "updated_at",
        ]


# 로그인 응답
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


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
