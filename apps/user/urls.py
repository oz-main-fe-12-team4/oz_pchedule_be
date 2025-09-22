from django.urls import path
from .views import (
    SignupView,
    LoginView,
    SocialLoginView,
    LogoutView,
    UserInfoView,
    UserEditView,
    UserDeleteView,
    TokenRefreshView,
    NicknameUpdateView,
    PasswordChangeView,
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("social-login", SocialLoginView.as_view(), name="social-login"),  # ✅ 소셜 로그인
    path("logout", LogoutView.as_view(), name="logout"),
    path("me", UserInfoView.as_view(), name="user-info"),
    path("me/edit", UserEditView.as_view(), name="user-edit"),
    path("me/withdraw", UserDeleteView.as_view(), name="user-delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    path("me/nickname", NicknameUpdateView.as_view(), name="user-nickname-update"),
    path("me/password", PasswordChangeView.as_view(), name="user-password-change"),
]
