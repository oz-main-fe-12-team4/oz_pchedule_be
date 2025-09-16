from django.urls import path
from .views import (
    ScheduleCreateView,
    ScheduleListView,
    ScheduleDetailView,
    RecurrenceCreateView,
    ScheduleCompleteView,
)

urlpatterns = [
    path("create/", ScheduleCreateView.as_view(), name="schedule-create"),
    path("list/", ScheduleListView.as_view(), name="schedule-list"),
    path("<int:pk>/", ScheduleDetailView.as_view(), name="schedule-detail"),
    path("<int:pk>/complete/", ScheduleCompleteView.as_view(), name="schedule-complete"),
    path("recurrence/create/", RecurrenceCreateView.as_view(), name="recurrence-create"),
]
