from django.urls import path
from .views import ScheduleCreateView, ScheduleListView, ScheduleDetailView

urlpatterns = [
    path("create/", ScheduleCreateView.as_view(), name="schedule-create"),
    path("list/", ScheduleListView.as_view(), name="schedule-list"),
    path("<int:pk>/", ScheduleDetailView.as_view(), name="schedule-detail"),
]
