from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.core.dummy_serializer import DummySerializer
from apps.notification.models import Notification
from .models import Bookmark, Like, Report
from apps.schedule.models import Schedule
from rest_framework.exceptions import NotFound
from .serializers import ReportSerializer


class ScheduleLikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DummySerializer

    def post(self, request, schedule_id):
        schedule = Schedule.objects.filter(id=schedule_id).first()
        if not schedule:
            raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

        try:
            # 좋아요 생성
            like, created = Like.objects.get_or_create(user=request.user, schedule=schedule)

            if created:
                # 알림 생성
                Notification.objects.create(
                    user=schedule.user,  # 알림 받는 사람: 일정 작성자
                    type="LIKE",  # 알림 타입 (임의로 LIKE로 지정)
                    content=f"{request.user.username}님이 '{schedule.title}' 일정에 좋아요를 눌렀습니다.",
                    is_read=False,
                )

            return Response(
                {"message": "좋아요에 추가되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ScheduleBookmarkAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DummySerializer

    def post(self, request, schedule_id):
        schedule = Schedule.objects.filter(id=schedule_id).first()
        if not schedule:
            raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

        try:
            # 찜 생성
            bookmark, created = Bookmark.objects.get_or_create(user=request.user, schedule=schedule)

            if created:
                # 알림 생성
                Notification.objects.create(
                    user=schedule.user,  # 알림 받는 사람: 일정 작성자
                    type="BOOKMARK",  # 알림 타입: BOOKMARK
                    content=f"{request.user.username}님이 '{schedule.title}' 일정에 찜을 추가했습니다.",
                    is_read=False,
                )

            return Response(
                {"message": "찜하기에 추가되었습니다."},
                status=status.HTTP_201_CREATED,
            )

        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ScheduleReportAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializer

    def post(self, request, schedule_id):
        schedule = Schedule.objects.filter(id=schedule_id).first()
        if not schedule:
            raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

        try:
            if Report.objects.filter(schedule=schedule).exists():
                return Response(
                    {"error": "이미 신고처리된 일정입니다."},
                    status=status.HTTP_409_CONFLICT,
                )

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # ✅ user는 ReportSerializer가 알아서 채움
            serializer.save(schedule=schedule)

            # 신고 알림 생성 (관리자 혹은 일정 작성자에게)
            Notification.objects.create(
                user=schedule.user,  # 알림 받는 사람: 일정 작성자
                type="REPORT",  # 알림 타입: REPORT
                content=f"{request.user.username}님이 '{schedule.title}' 일정을 신고했습니다.",
                is_read=False,
            )

            return Response(
                {"message": "신고가 접수되었습니다."},
                status=status.HTTP_201_CREATED,
            )

        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
