# urls.py
from django.urls import path
from .views import (
    ScheduleListAPIView,
    ScheduleCreateAPIView,
    DetailScheduleUpdateDeleteAPIView,
)

urlpatterns = [
    # 일정 전체 조회
    path("schedules/", ScheduleListAPIView.as_view(), name="schedule-list"),
    # 일정 생성
    path("schedules/create/", ScheduleCreateAPIView.as_view(), name="schedule-create"),
    # 일정 상세 조회 / 수정 / 삭제 / 완료 토글
    path("schedules/<int:pk>/", DetailScheduleUpdateDeleteAPIView.as_view(), name="schedule-detail"),
]
