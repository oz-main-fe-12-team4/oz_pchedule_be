from django.urls import path
from .views import (
    SignupView,
    LoginView,
    SocialLoginView,
    LogoutView,
    UserInfoView,
    UserNameEditView,  # 닉네임 수정
    UserPasswordEditView,  # 비밀번호 수정
    UserDeleteView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("social-login", SocialLoginView.as_view(), name="social-login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("me", UserInfoView.as_view(), name="user-info"),
    path("me/nickname", UserNameEditView.as_view(), name="user-nickname-edit"),
    path("me/password", UserPasswordEditView.as_view(), name="user-password-edit"),
    path("me/withdraw", UserDeleteView.as_view(), name="user-delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
