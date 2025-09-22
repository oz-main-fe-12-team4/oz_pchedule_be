from django.urls import path
from .views import (
    SignupView,
    LoginView,
    LogoutView,
    UserInfoView,
    UserNameEditView,
    UserPasswordEditView,
    UserDeleteView,
    TokenRefreshView,
)

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("me", UserInfoView.as_view(), name="user-info"),
    path("me/edit/name", UserNameEditView.as_view(), name="user-edit-name"),
    path("me/edit/password", UserPasswordEditView.as_view(), name="user-edit-password"),
    path("me/withdraw", UserDeleteView.as_view(), name="user-delete"),
    path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
]
