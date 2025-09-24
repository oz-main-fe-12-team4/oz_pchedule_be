from rest_framework import serializers
from .models import User, LoginAttempt, Token, TokenBlacklist


# 회원가입 / 유저 생성
class UserSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)
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


# 로그인 요청
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# 로그인 응답
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


# 로그아웃
class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


#  에러 응답
class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField()


# 닉네임
class ChangeNameSerializer(serializers.Serializer):
    name = serializers.CharField()


# 패스워드 변경
class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)


# 내 정보 조회 응답
class UserInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="id", read_only=True)
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


# 관리자 전용 유저 리스트 응답
class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "is_active", "is_reported", "report_reason"]


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
        model = TokenBlacklist
        fields = "__all__"
