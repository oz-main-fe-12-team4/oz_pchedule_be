from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User, LoginAttempt

from ..interactions.models import Report


# 회원가입 / 유저 생성
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "name",
        ]


# 로그인 요청
class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


# 로그인 응답
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    is_admin = serializers.BooleanField()


# 소셜 로그인
class SocialLoginSerializer(serializers.Serializer):
    provider = serializers.ChoiceField(choices=["kakao", "google", "naver"])
    access_token = serializers.CharField()


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
    id = serializers.IntegerField(read_only=True)
    total_like = serializers.IntegerField(default=0)
    total_bookmark = serializers.IntegerField(default=0)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "profile_image",
            "allow_notification",
            "total_like",
            "total_bookmark",
        ]


# 관리자 전용 유저 리스트 응답
class UserAdminSerializer(serializers.ModelSerializer):
    report_reason = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "email", "name", "is_admin", "report_reason"]

    def get_report_reason(self, obj):
        # User 와 연결된 Report 모델에서 이유만 뽑아내기
        report = Report.objects.filter(user=obj).first()
        return report.reason if report else None


# 로그인 시도 기록
class LoginAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoginAttempt
        fields = "__all__"


# is_admin 토큰
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["is_admin"] = user.is_admin  # 토큰 payload에 포함
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data["is_admin"] = self.user.is_admin  # 응답에 추가
        return data
