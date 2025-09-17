from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Schedule, Recurrence
from .serializers import ScheduleSerializer, RecurrenceSerializer


# 일정 추가
class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 일정 조회
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


# 일정 상세/수정/삭제
class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


# 반복 일정 추가
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
