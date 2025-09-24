from django.urls import path
from .views import (
    ScheduleListCreateAPIView,
    ScheduleDetailAPIView,
    DetailScheduleCompleteAPIView,
    DetailScheduleUpdateDeleteAPIView,
)

urlpatterns = [
    # 일정 목록 조회 / 생성
    path("schedules", ScheduleListCreateAPIView.as_view(), name="schedule-list-create"),
    # 일정 상세 조회 / 수정 / 삭제
    path("schedules/<int:schedule_id>", ScheduleDetailAPIView.as_view(), name="schedule-detail"),
    # 세부 일정 완료 처리
    path(
        "detail-schedules/<int:detail_id>/complete",
        DetailScheduleCompleteAPIView.as_view(),
        name="detail-schedule-complete",
    ),
    # 세부 일정 수정 / 삭제
    path(
        "detail-schedules/<int:detail_id>",
        DetailScheduleUpdateDeleteAPIView.as_view(),
        name="detail-schedule-update-delete",
    ),
]
