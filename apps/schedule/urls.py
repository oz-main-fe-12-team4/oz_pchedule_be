from django.urls import path
from .views import (
    ScheduleListAPIView,
    ScheduleCreateAPIView,
    ScheduleDetailAPIView,
    DetailScheduleCompleteAPIView,
)

urlpatterns = [
    path("schedules/", ScheduleListAPIView.as_view(), name="schedule-list"),
    path("schedules/create/", ScheduleCreateAPIView.as_view(), name="schedule-create"),
    path("schedules/<int:pk>/", ScheduleDetailAPIView.as_view(), name="schedule-detail"),
    path("details/<int:pk>/complete/", DetailScheduleCompleteAPIView.as_view(), name="detail-complete"),
]
