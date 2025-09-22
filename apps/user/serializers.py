from rest_framework import serializers
from .models import User, LoginAttempt, Token, AccessTokenBlacklist


# 회원가입 / 유저 생성
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user_id", read_only=True)  # PK 매핑 명확히
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "user_id",
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
    data = serializers.DictField()  # {"access_token": "...", "refresh_token": "..."}


# 내 정보 조회 응답
class UserInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user_id", read_only=True)
    total_like = serializers.IntegerField(default=0)
    total_bookmark = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = [
            "user_id",
            "email",
            "name",
            "profile_image",
            "allow_notification",
            "total_like",
            "total_bookmark",
        ]


# 토큰
class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = "__all__"


# 로그인 시도 기록
class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = "__all__"


# 블랙리스트 처리된 AccessToken
class AccessTokenBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessTokenBlacklist
        fields = "__all__"
