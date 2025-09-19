from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ScheduleViewSet, DetailScheduleViewSet, RecurrenceViewSet, WeekdayViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("weekdays", WeekdayViewSet)
router.register("schedules", ScheduleViewSet)
router.register("details", DetailScheduleViewSet)
router.register("recurrences", RecurrenceViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
