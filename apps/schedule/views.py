from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer


# 일정 추가
class ScheduleCreateView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 일정 조회 (유저별)
class ScheduleListView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)


# 일정 상세/수정/삭제
class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    queryset = Schedule.objects.all()

    def get_queryset(self):
        # 유저 본인의 일정만
        return Schedule.objects.filter(user=self.request.user)
