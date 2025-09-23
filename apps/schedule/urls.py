from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    WeekdayViewSet,
    ScheduleViewSet,
    DetailScheduleViewSet,
    RecurrenceViewSet,
)

router = DefaultRouter()
router.register(r"schedule/categories", CategoryViewSet, basename="category")
router.register(r"schedule/weekdays", WeekdayViewSet, basename="weekday")
router.register(r"schedule/schedules", ScheduleViewSet, basename="schedule")
router.register(r"schedule/details", DetailScheduleViewSet, basename="detailschedule")
router.register(r"schedule/recurrences", RecurrenceViewSet, basename="recurrence")

urlpatterns = [
    path("", include(router.urls)),
]
