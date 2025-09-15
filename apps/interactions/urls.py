from django.urls import path

from apps.interactions.views import PostFavoriteAPIView, PostLikeAPIView, PostReportAPIView

urlpatterns = [
    path("post/{post_id}/like", PostLikeAPIView.as_view(), name="transactions-like"),
    path("post/{post_id}/favorite", PostFavoriteAPIView.as_view(), name="transactions-favorite"),
    path("post/{post_id}/report", PostReportAPIView.as_view(), name="transactions-report"),
]
