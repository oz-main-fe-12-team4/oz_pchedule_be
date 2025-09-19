from rest_framework import serializers
from .models import User, LoginAttempt, Token, AccessTokenBlacklist


# 회원가입 / 유저 생성 시 사용
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)  # user_id 반환
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "password",
            "name",
            "profile_image",
            "created_at",
            "updated_at",
        ]


# 로그인 응답
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    data = serializers.DictField()  # {"access_token": "...", "refresh_token": "..."}


# 내 정보 조회 응답
class UserInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)
    total_like = serializers.IntegerField(default=0)
    total_favorite = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "name",
            "profile_image",
            "total_like",
            "total_favorite",
        ]


# 로그인 시도 기록 (내부용)
class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = "__all__"


# 토큰 저장 (내부용)
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


# Access Token 블랙리스트 (내부용)
class AccessTokenBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTokenBlacklist
        fields = "__all__"
