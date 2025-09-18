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
    path("<int:user_id>/logout", LogoutView.as_view(), name="logout"),
    path("<int:user_id>/info", UserInfoView.as_view(), name="user-info"),
    path("<int:user_id>/edit", UserEditView.as_view(), name="user-edit"),
    path("<int:user_id>/delete", UserDeleteView.as_view(), name="user-delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
