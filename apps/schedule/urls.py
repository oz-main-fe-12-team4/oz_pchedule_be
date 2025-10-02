from django.urls import path
from .views import (
    ScheduleListCreateAPIView,
    ScheduleRetrieveUpdateDestroyAPIView,
    DetailScheduleListCreateAPIView,
    DetailScheduleRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    # Schedule (GET, POST)
    path("schedules/", ScheduleListCreateAPIView.as_view(), name="schedule-list-create"),
    # Schedule (GET, PUT, DELETE)
    path("schedules/<int:pk>/", ScheduleRetrieveUpdateDestroyAPIView.as_view(), name="schedule-rud"),
    # DetailSchedule (GET, POST)
    path("details/", DetailScheduleListCreateAPIView.as_view(), name="detail-list-create"),
    # DetailSchedule (GET, PUT, DELETE)
    path("details/<int:pk>/", DetailScheduleRetrieveUpdateDestroyAPIView.as_view(), name="detail-rud"),
]
