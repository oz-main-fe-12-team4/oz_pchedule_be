from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, LoginAttempt, Token, AccessTokenBlacklist
from .serializers import (
    UserSerializer,
    LoginAttemptSerializer,
    TokenSerializer,
    AccessTokenBlacklistSerializer,
)


# 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = serializer.validated_data.get("password")
        serializer.save(password=make_password(password))


# 로그인 (JWT 발급 + LoginAttempt 기록)
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            # refresh_token DB 저장
            Token.objects.create(
                user=user, refresh_token=str(refresh), expires_at=refresh.access_token.payload["exp"], is_revoked=False
            )
            # 로그인 성공 기록
            LoginAttempt.objects.create(user=user, is_success=True, ip_address=request.META.get("REMOTE_ADDR"))
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)}, status=status.HTTP_200_OK)
        else:
            # 실패 기록
            db_user = User.objects.filter(email=email).first()
            LoginAttempt.objects.create(user=db_user, is_success=False, ip_address=request.META.get("REMOTE_ADDR"))
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


# 로그아웃 (AccessToken 블랙리스트 등록)
class LogoutView(APIView):
    def post(self, request):
        token = request.data.get("token")  # 현재 사용 중인 access token
        user = request.user
        if token and user.is_authenticated:
            AccessTokenBlacklist.objects.create(user=user, access_token=token)
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
