from django.urls import path

from apps.interactions.views import ScheduleBookmarkAPIView, ScheduleLikeAPIView, ScheduleReportAPIView

urlpatterns = [
    path("like", ScheduleLikeAPIView.as_view(), name="like"),
    path("unlike", ScheduleLikeAPIView.as_view(), name="unlike"),
    path("bookmark", ScheduleBookmarkAPIView.as_view(), name="bookmark"),
    path("report", ScheduleReportAPIView.as_view(), name="report"),
]
