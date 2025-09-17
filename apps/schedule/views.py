from django.utils.dateparse import parse_datetime
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .models import Schedule
from .serializers import ScheduleSerializer, RecurrenceSerializer


# 일정 생성
class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 일정 목록
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


# 일정 상세 조회 / 수정 / 삭제
class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


# 반복 일정 생성
class RecurrenceCreateView(generics.CreateAPIView):
    serializer_class = RecurrenceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        schedule_id = self.request.data.get("schedule")
        schedule = Schedule.objects.get(id=schedule_id, user=self.request.user)
        serializer.save(schedule=schedule)


# 일정 완료 처리
class ScheduleCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            schedule = Schedule.objects.get(pk=pk, user=request.user)
            schedule.is_completed = True
            schedule.save()
            return Response({"message": "일정이 완료되었습니다."}, status=status.HTTP_200_OK)
        except Schedule.DoesNotExist:
            return Response({"error": "일정을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)


# 일정 중복 체크
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def schedule_overlap_check(request):
    start_time_str = request.query_params.get("start_time")
    end_time_str = request.query_params.get("end_time")

    if not start_time_str or not end_time_str:
        return Response({"error": "start_time과 end_time을 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)

    start_time = parse_datetime(start_time_str)
    end_time = parse_datetime(end_time_str)

    if not start_time or not end_time:
        return Response(
            {"error": "시간 형식이 잘못되었습니다. (YYYY-MM-DDTHH:MM:SS)"}, status=status.HTTP_400_BAD_REQUEST
        )

    conflicts = Schedule.objects.filter(user=request.user, start_time__lt=end_time, end_time__gt=start_time)

    if conflicts.exists():
        serializer = ScheduleSerializer(conflicts, many=True)
        return Response({"overlap": True, "conflicts": serializer.data}, status=status.HTTP_200_OK)
    else:
        return Response({"overlap": False, "conflicts": []}, status=status.HTTP_200_OK)
