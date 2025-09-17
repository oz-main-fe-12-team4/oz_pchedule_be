from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostDetailView,
    post_like,
    post_favorite,
    post_report,
)

urlpatterns = [
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("list/", PostListView.as_view(), name="post-list"),
    path("<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("<int:pk>/like/", post_like, name="post-like"),
    path("<int:pk>/favorite/", post_favorite, name="post-favorite"),
    path("<int:pk>/report/", post_report, name="post-report"),
]
