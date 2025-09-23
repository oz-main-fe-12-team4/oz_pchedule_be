# apps/schedule/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    WeekdayViewSet,
    ScheduleViewSet,
    DetailScheduleViewSet,
    RecurrenceViewSet,
)

# DRF DefaultRouter 생성
router = DefaultRouter()
router.register("categories", CategoryViewSet)
router.register("weekdays", WeekdayViewSet)
router.register("schedules", ScheduleViewSet)
router.register("details", DetailScheduleViewSet)
router.register("recurrences", RecurrenceViewSet)

# URL 패턴 등록
urlpatterns = [
    path("", include(router.urls)),
]
