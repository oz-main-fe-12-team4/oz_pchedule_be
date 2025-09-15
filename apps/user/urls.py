from django.urls import path
from .views import (
    RegisterView,
    UserListCreateView,
    UserDetailView,
    LoginAttemptListView,
    TokenListCreateView,
    AccessTokenBlacklistListCreateView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("users/", UserListCreateView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("login-attempts/", LoginAttemptListView.as_view(), name="login-attempt-list"),
    path("tokens/", TokenListCreateView.as_view(), name="token-list"),
    path("blacklist/", AccessTokenBlacklistListCreateView.as_view(), name="blacklist-list"),
]
