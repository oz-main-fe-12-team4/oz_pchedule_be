from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, RecurrenceViewSet

router = DefaultRouter()
router.register(r"schedules", ScheduleViewSet, basename="schedule")
router.register(r"recurrences", RecurrenceViewSet, basename="recurrence")

urlpatterns = [
    path("", include(router.urls)),
]
