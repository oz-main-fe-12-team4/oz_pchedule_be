from django.urls import path

from apps.interactions.views import PostFavoriteAPIView, PostLikeAPIView, PostReportAPIView

urlpatterns = [
    path("post/<int:pk>/like", PostLikeAPIView.as_view(), name="transactions-like"),
    path("post/<int:pk>/favorite", PostFavoriteAPIView.as_view(), name="transactions-favorite"),
    path("post/<int:pk>/report", PostReportAPIView.as_view(), name="transactions-report"),
]
