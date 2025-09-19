from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Bookmark, Like, Report
from apps.schedule.models import Schedule
from rest_framework.exceptions import NotFound
from .serializers import ReportSerializer


class ScheduleLikeAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, schedule_id):
        schedule = Schedule.objects.filter(id=schedule_id).first()
        if not schedule:
            raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

        try:
            Like.objects.get_or_create(user=request.user, schedule=schedule)
            return Response(
                {"message": "좋아요에 추가되었습니다."},
                status=status.HTTP_201_CREATED,
            )
        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, schedule_id):
        try:
            schedule = Schedule.objects.filter(id=schedule_id).first()
            if not schedule:
                raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

            Like.objects.filter(user=request.user, schedule=schedule).delete()

            return Response(
                {"message": "좋아요에서 제거되었습니다."},
                status=status.HTTP_200_OK,
            )

        except NotFound as e:
            return Response(e.detail, status=status.HTTP_404_NOT_FOUND)

        except Exception:
            return Response(
                {"error": "예기치 못한 서버 오류가 발생했습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ScheduleBookmarkAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, schedule_id):
        try:
            schedule = Schedule.objects.filter(id=schedule_id).first()
            if not schedule:
                raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

            Bookmark.objects.get_or_create(user=request.user, schedule=schedule)

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
        try:
            schedule = Schedule.objects.filter(id=schedule_id).first()
            if not schedule:
                raise NotFound(detail={"error": "해당 일정이 존재하지 않습니다."})

            if Report.objects.filter(schedule=schedule).exists():
                return Response(
                    {"error": "이미 신고처리된 일정입니다."},
                    status=status.HTTP_409_CONFLICT,
                )

            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                return Response(
                    {"error": "잘못된 형식의 요청입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer.save(user=request.user, schedule=schedule)

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
