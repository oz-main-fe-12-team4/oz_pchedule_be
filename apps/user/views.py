import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, LoginAttempt, Token, AccessTokenBlacklist
from .serializers import UserSerializer


# 회원가입
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        name = serializer.validated_data.get("name")

        try:
            # 중복 검사
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"error": "이메일 또는 닉네임이 중복되었습니다."},
                    code=status.HTTP_409_CONFLICT,
                )
            if User.objects.filter(name=name).exists():
                raise serializers.ValidationError(
                    {"error": "이메일 또는 닉네임이 중복되었습니다."},
                    code=status.HTTP_409_CONFLICT,
                )

            password = serializer.validated_data.get("password")
            if not password or len(password) < 6:
                raise serializers.ValidationError(
                    {"error": "이메일 또는 닉네임 또는 비밀번호의 유효성 검사를 통과하지 못했습니다."},
                    code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

            serializer.save(password=make_password(password))

        except serializers.ValidationError:
            raise
        except Exception:
            raise serializers.ValidationError(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 로그인
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "이메일 또는 비밀번호를 확인해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 로그인 시도 제한
        attempts = LoginAttempt.objects.filter(
            ip_address=request.META.get("REMOTE_ADDR"),
            login_attempt_time__gte=timezone.now() - timedelta(minutes=5),
            is_success=False,
        ).count()
        if attempts >= 5:
            return Response(
                {"error": "부적절한 로그인 시도입니다."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        user = authenticate(request, email=email, password=password)
        if user is None:
            LoginAttempt.objects.create(
                user=None,
                is_success=False,
                ip_address=request.META.get("REMOTE_ADDR"),
            )
            return Response(
                {"error": "이메일이 존재하지 않거나 비밀번호가 틀렸습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.is_locked:
            return Response(
                {"error": "정지된 계정입니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 토큰 발급 (access만 반환)
        refresh = RefreshToken.for_user(user)
        Token.objects.create(
            user=user,
            refresh_token=str(refresh),
            expires_at=datetime.fromtimestamp(refresh.access_token.payload["exp"]),
            is_revoked=False,
        )
        LoginAttempt.objects.create(
            user=user,
            is_success=True,
            ip_address=request.META.get("REMOTE_ADDR"),
        )

        return Response(
            {
                "message": "로그인이 완료되었습니다.",
                "data": {"access_token": str(refresh.access_token)},
            },
            status=status.HTTP_200_OK,
        )


# 소셜 로그인
class SocialLoginView(APIView):
    def post(self, request):
        provider = request.data.get("provider")
        access_token = request.data.get("access_token")

        try:
            if provider == "kakao":
                url = "https://kapi.kakao.com/v2/user/me"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response(
                        {"error": "소셜 토큰 인증에 실패했습니다."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                data = response.json()
                email = data.get("kakao_account", {}).get("email", f"kakao_{data['id']}@example.com")
                name = data.get("properties", {}).get("nickname", f"user_{data['id']}")

            elif provider == "google":
                url = "https://www.googleapis.com/oauth2/v3/userinfo"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response(
                        {"error": "소셜 토큰 인증에 실패했습니다."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                data = response.json()
                email = data.get("email")
                name = data.get("name", email.split("@")[0])

            elif provider == "naver":
                url = "https://openapi.naver.com/v1/nid/me"
                headers = {"Authorization": f"Bearer {access_token}"}
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    return Response(
                        {"error": "소셜 토큰 인증에 실패했습니다."},
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
                data = response.json().get("response", {})
                email = data.get("email")
                name = data.get("nickname", email.split("@")[0] if email else "naver_user")

            else:
                return Response(
                    {"error": "지원하지 않는 provider"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

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
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = request.auth
        if token:
            AccessTokenBlacklist.objects.create(user=request.user, access_token=str(token))
            return Response({"message": "로그아웃이 완료되었습니다."}, status=status.HTTP_200_OK)
        return Response({"error": "토큰 인증에 실패했습니다."}, status=status.HTTP_401_UNAUTHORIZED)


# 내 정보 조회
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "user_id": request.user.id,
            "email": request.user.email,
            "name": request.user.name,
            "profile_image": request.user.profile_image,
            "allow_notification": request.user.allow_notification,
            "total_like": 0,
            "total_favorite": 0,
        }
        return Response({"data": data}, status=status.HTTP_200_OK)


# 내 정보 수정
class UserEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        name = request.data.get("name")
        password = request.data.get("password")

        try:
            if name and User.objects.exclude(id=request.user.id).filter(name=name).exists():
                return Response(
                    {"error": "중복된 닉네임입니다."},
                    status=status.HTTP_409_CONFLICT,
                )

            if name:
                request.user.name = name
            if password:
                request.user.password = make_password(password)

            request.user.save()
            return Response({"message": "정보가 수정되었습니다."}, status=status.HTTP_200_OK)

        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 회원 탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            request.user.delete()
            return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# 토큰 재발급
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"error": "잘못된 형식의 요청입니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token
            return Response(
                {"data": {"access_token": str(new_access)}},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"error": "토큰 인증에 실패했습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
