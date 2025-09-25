from django.urls import path
from .views import (
    ScheduleListCreateAPIView,
    ScheduleDetailAPIView,
    DetailScheduleCompleteAPIView,
    DetailScheduleUpdateDeleteAPIView,
)

urlpatterns = [
    path("schedules", ScheduleListCreateAPIView.as_view(), name="schedule-list-create"),
    path("schedules/<int:schedule_id>", ScheduleDetailAPIView.as_view(), name="schedule-detail"),
    path(
        "detail-schedules/<int:detail_id>/complete",
        DetailScheduleCompleteAPIView.as_view(),
        name="detail-schedule-complete",
    ),
    path(
        "detail-schedules/<int:detail_id>",
        DetailScheduleUpdateDeleteAPIView.as_view(),
        name="detail-schedule-update-delete",
    ),
]
