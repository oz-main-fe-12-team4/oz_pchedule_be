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
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("social-login", SocialLoginView.as_view(), name="social-login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("me", UserInfoView.as_view(), name="user-info"),
    path("me/edit", UserEditView.as_view(), name="user-edit"),
    path("me/withdraw", UserDeleteView.as_view(), name="user-delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
