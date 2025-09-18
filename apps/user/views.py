import requests
from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from .models import User, LoginAttempt, Token, AccessTokenBlacklist
from .serializers import UserSerializer


# 회원가입
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        email = serializer.validated_data.get("email")
        name = serializer.validated_data.get("name")

        # 이메일/닉네임 중복 검사
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"message": "이미 사용 중인 이메일입니다."},
                code=status.HTTP_409_CONFLICT,
            )
        if User.objects.filter(name=name).exists():
            raise serializers.ValidationError(
                {"message": "이미 사용 중인 닉네임입니다."},
                code=status.HTTP_409_CONFLICT,
            )

        password = serializer.validated_data.get("password")
        serializer.save(password=make_password(password))


# 로그인
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        # 잘못된 요청
        if not email or not password:
            return Response(
                {"message": "이메일과 비밀번호를 입력해주세요"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 로그인 시도 제한 (5분 내 5회 이상 실패)
        attempts = LoginAttempt.objects.filter(
            ip_address=request.META.get("REMOTE_ADDR"),
            login_attempt_time__gte=timezone.now() - timedelta(minutes=5),
            is_success=False,
        ).count()
        if attempts >= 5:
            return Response(
                {"message": "짧은 시간 내 과도한 로그인 시도"},
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
                {"message": "이메일이나 비밀번호를 확인해주세요"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if user.is_locked:
            return Response(
                {"message": "정지된 계정입니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        # 토큰 발급
        refresh = RefreshToken.for_user(user)
        Token.objects.create(
            user=user,
            refresh_token=str(refresh),
            expires_at=refresh.access_token.payload["exp"],
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
                "data": {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


# 소셜 로그인 (카카오, 구글, 네이버)
class SocialLoginView(APIView):
    def post(self, request):
        provider = request.data.get("provider")
        access_token = request.data.get("access_token")

        if provider == "kakao":
            url = "https://kapi.kakao.com/v2/user/me"
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return Response(
                    {"message": "소셜 토큰 인증 실패"},
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
                    {"message": "소셜 토큰 인증 실패"},
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
                    {"message": "소셜 토큰 인증 실패"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            data = response.json().get("response", {})
            email = data.get("email")
            name = data.get("nickname", email.split("@")[0] if email else "naver_user")

        else:
            return Response(
                {"message": "지원하지 않는 provider"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "password": make_password(User.objects.make_random_password()),
            },
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "소셜 로그인이 완료되었습니다.",
                "data": {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


# 로그아웃
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        token = request.auth
        if token:
            AccessTokenBlacklist.objects.create(user=request.user, access_token=str(token))
            return Response(
                {"message": "로그아웃이 완료되었습니다."},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "토큰 인증 실패"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# 내 정보 조회
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        if request.user.id != int(user_id):
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = {
            "user_id": request.user.id,
            "email": request.user.email,
            "name": request.user.name,
            "profile_image": request.user.profile_image,
            "allow_notification": request.user.allow_notification,
            "total_like": 0,  # TODO: 실제 로직 연동
            "total_favorite": 0,  # TODO: 실제 로직 연동
        }
        return Response({"data": data}, status=status.HTTP_200_OK)


# 내 정보 수정
class UserEditView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, user_id):
        if request.user.id != int(user_id):
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        name = request.data.get("name")
        password = request.data.get("password")

        if name and User.objects.exclude(id=user_id).filter(name=name).exists():
            return Response(
                {"message": "닉네임이 중복되었습니다."},
                status=status.HTTP_409_CONFLICT,
            )

        if name:
            request.user.name = name
        if password:
            request.user.password = make_password(password)

        request.user.save()
        return Response(
            {"message": "정보가 수정되었습니다."},
            status=status.HTTP_200_OK,
        )


# 회원 탈퇴
class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        if request.user.id != int(user_id):
            return Response(
                {"message": "권한이 없습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        request.user.delete()
        return Response(
            {"message": "회원 탈퇴가 완료되었습니다."},
            status=status.HTTP_200_OK,
        )


# 토큰 재발급
class TokenRefreshView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if not refresh_token:
            return Response(
                {"message": "잘못된 요청입니다."},
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
                {"message": "토큰 인증 실패"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
