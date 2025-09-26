import requests
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User, LoginAttempt
from .permissions import IsCustomAdmin
from .serializers import (
    UserSerializer,
    UserInfoSerializer,
    LoginAttemptSerializer,
    UserAdminSerializer,
    LoginRequestSerializer,
    ChangeNameSerializer,
    ChangePasswordSerializer,
    SocialLoginSerializer,
    CustomTokenObtainPairSerializer,
    LoginResponseSerializer,
)


# ---------------- 회원 관련 ---------------- #
# 회원가입
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        name = serializer.validated_data.get("name")

        try:
            errors = []

            if User.objects.filter(email=email).exists():
                errors.append("이메일이 중복되었습니다.")

            if User.objects.filter(name=name).exists():
                errors.append("닉네임이 중복되었습니다.")

            if errors:
                return Response({"errors": errors}, status=status.HTTP_409_CONFLICT)

            password = serializer.validated_data.get("password")
            if not password or len(password) < 6:
                return Response(
                    {"error": "비밀번호는 최소 6자리 이상이어야 합니다."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            # 저장 (비밀번호 해싱 포함)
            self.perform_create(serializer)

        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"message": "회원가입이 완료되었습니다."},
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        password = serializer.validated_data.get("password")
        serializer.save(password=make_password(password))


class LoginView(generics.GenericAPIView):
    serializer_class = LoginRequestSerializer  # ✅ 요청 Body용 Serializer 지정

    @swagger_auto_schema(
        request_body=LoginRequestSerializer,  # 요청 바디 스키마
        responses={
            200: LoginResponseSerializer,  # ✅ 응답 스키마를 시리얼라이저로 교체
            400: "잘못된 요청 (이메일/비밀번호 누락)",
            401: "이메일 또는 비밀번호가 올바르지 않음",
            403: "정지된 계정",
            429: "로그인 시도 제한 초과",
        },
        operation_description="사용자 로그인 (이메일 + 비밀번호, HttpOnly Cookie에 토큰 저장)",
    )
    def post(self, request):
        # ✅ 요청 데이터 검증
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        # 로그인 시도 제한 (5분 내 5회 실패 시 차단)
        attempts = LoginAttempt.objects.filter(
            ip_address=request.META.get("REMOTE_ADDR"),
            login_attempt_time__gte=timezone.now() - timezone.timedelta(minutes=5),
            is_success=False,
        ).count()
        if attempts >= 5:
            return Response(
                {"error": "부적절한 로그인 시도입니다."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # 사용자 인증
        user = authenticate(request, username=email, password=password)
        if user is None:
            login_attempt_data = {
                "user": None,
                "is_success": False,
                "ip_address": request.META.get("REMOTE_ADDR"),
            }
            attempt_serializer = LoginAttemptSerializer(data=login_attempt_data)
            attempt_serializer.is_valid(raise_exception=True)
            attempt_serializer.save()

            return Response(
                {"error": "이메일이 존재하지 않거나 비밀번호가 틀렸습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if getattr(user, "is_locked", False):
            return Response(
                {"error": "정지된 계정입니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # ✅ JWT 발급
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        # 성공한 로그인 기록
        login_attempt_data = {
            "user": user.id,
            "is_success": True,
            "ip_address": request.META.get("REMOTE_ADDR"),
        }
        success_serializer = LoginAttemptSerializer(data=login_attempt_data)
        success_serializer.is_valid(raise_exception=True)
        success_serializer.save()

        # ✅ 응답 데이터 (시리얼라이저 활용)
        response_data = {"message": "로그인이 완료되었습니다.", "is_admin": user.is_admin}
        response_serializer = LoginResponseSerializer(response_data)

        response = Response(response_serializer.data, status=status.HTTP_200_OK)

        # Access Token 쿠키 저장
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 5,
        )

        # Refresh Token 쿠키 저장 (추가 권장)
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
        )

        return response


# ✅ 소셜 로그인
class SocialLoginView(generics.GenericAPIView):
    serializer_class = SocialLoginSerializer  # ✅ swagger에 request body 노출됨

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        provider = serializer.validated_data["provider"]
        access_token = serializer.validated_data["access_token"]

        try:
            if provider == "kakao":
                url = "https://kapi.kakao.com/v2/user/me"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response({"error": "소셜 토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
                data = response.json()
                email = data.get("kakao_account", {}).get("email", f"kakao_{data['id']}@example.com")
                name = data.get("properties", {}).get("nickname", f"user_{data['id']}")

            elif provider == "google":
                url = "https://www.googleapis.com/oauth2/v3/userinfo"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response({"error": "소셜 토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
                data = response.json()
                email = data.get("email")
                name = data.get("name", email.split("@")[0])

            elif provider == "naver":
                url = "https://openapi.naver.com/v1/nid/me"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response({"error": "소셜 토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)
                data = response.json().get("response", {})
                email = data.get("email")
                name = data.get("nickname", email.split("@")[0] if email else "naver_user")

            else:
                return Response({"error": "지원하지 않는 provider"}, status=status.HTTP_400_BAD_REQUEST)

            user, _ = User.objects.get_or_create(
                email=email,
                defaults={"name": name, "password": make_password(User.objects.make_random_password())},
            )

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "소셜 로그인이 완료되었습니다.",
                    "data": {"access_token": str(refresh.access_token)},
                },
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ 로그아웃
class LogoutView(generics.GenericAPIView):

    def post(self, request):
        refresh_token = request.COOKIES["refresh_token"]
        if not refresh_token:
            return Response({"error": "refresh_token이 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # ✅ refresh_token 블랙리스트에 등록
            return Response({"message": "로그아웃이 완료되었습니다."}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# ✅ 내 정보 조회
class UserInfoView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# 이름 변경
class UserNameEditView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeNameSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        name = serializer.validated_data.get("name")

        if User.objects.exclude(id=request.user.id).filter(name=name).exists():
            return Response({"error": "중복된 닉네임입니다."}, status=status.HTTP_409_CONFLICT)

        request.user.name = name
        request.user.save()

        return Response({"message": "이름이 수정되었습니다."}, status=status.HTTP_200_OK)


# ✅ 비밀번호 변경
class UserPasswordEditView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_password = serializer.validated_data["current_password"]
        new_password = serializer.validated_data["new_password"]
        confirm_password = serializer.validated_data["new_password_confirm"]

        # 현재 비밀번호 확인
        if not request.user.check_password(current_password):
            return Response(
                {"error": "현재 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # 새 비밀번호와 확인 비밀번호 일치 여부 확인
        if new_password != confirm_password:
            return Response(
                {"error": "비밀번호 확인이 일치하지 않습니다."},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        # 비밀번호 변경
        request.user.password = make_password(new_password)
        request.user.save()

        return Response(
            {"message": "비밀번호가 수정되었습니다."},
            status=status.HTTP_200_OK,
        )


# ✅ 회원 탈퇴
class UserDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            request.user.delete()
            return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ✅ 토큰 재발급
class TokenRefreshView(generics.GenericAPIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response({"error": "잘못된 형식의 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            return Response({"data": {"access_token": str(new_access)}}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# ---------------- 관리자 전용 ---------------- #


class UserListView(generics.GenericAPIView):
    permission_classes = [IsCustomAdmin]

    def get(self, request):
        if not request.user.is_admin:
            return Response({"error": "관리자 권한이 필요합니다."}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserAdminSerializer(users, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class UserActivateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if not request.user.is_admin:
            return Response({"error": "관리자 권한이 필요합니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            user.is_active = True
            user.save()
            return Response({"message": "계정이 활성화되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class UserDeactivateView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        if not request.user.is_admin:
            return Response({"error": "관리자 권한이 필요합니다."}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(id=user_id)
            user.is_active = False
            user.save()
            return Response({"message": "계정이 비활성화되었습니다."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "해당 유저가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
