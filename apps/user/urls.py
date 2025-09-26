from django.urls import path
from .views import (
    SignupView,
    LoginView,
    SocialLoginView,
    LogoutView,
    UserInfoView,
    UserNameEditView,
    UserPasswordEditView,
    UserDeleteView,
    UserListView,
    UserActivateView,
    UserDeactivateView,
)

urlpatterns = [
    # 회원 관련
    path("signup", SignupView.as_view(), name="user-signup"),
    path("login", LoginView.as_view(), name="user-login"),
    path("social-login", SocialLoginView.as_view(), name="user-social-login"),
    path("logout", LogoutView.as_view(), name="user-logout"),
    path("me", UserInfoView.as_view(), name="user-info"),
    path("me/name", UserNameEditView.as_view(), name="user-name-update"),
    path("me/password", UserPasswordEditView.as_view(), name="user-password-change"),
    path("me/withdraw", UserDeleteView.as_view(), name="user-delete"),
    # path("token/refresh", TokenRefreshView.as_view(), name="token-refresh"),
    # 관리자 전용
    path("users", UserListView.as_view(), name="admin-user-list"),
    path("users/<int:user_id>/activate", UserActivateView.as_view(), name="admin-user-activate"),
    path("users/<int:user_id>/deactivate", UserDeactivateView.as_view(), name="admin-user-deactivate"),
]
