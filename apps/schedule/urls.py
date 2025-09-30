from django.urls import path
from .views import (
    ScheduleListAPIView,
    ScheduleCreateAPIView,
    ScheduleDetailAPIView,
)

urlpatterns = [
    # 일정 조회 (리스트)
    path("schedules/", ScheduleListAPIView.as_view(), name="schedule-list"),
    # 일정 생성
    path("schedules/create/", ScheduleCreateAPIView.as_view(), name="schedule-create"),
    # 일정 상세 조회/수정/삭제
    path("schedules/<int:pk>/", ScheduleDetailAPIView.as_view(), name="schedule-detail"),
]
