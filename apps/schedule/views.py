from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer


# 일정 리스트 조회
class ScheduleListAPIView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# 일정 생성
class ScheduleCreateAPIView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


# 일정 상세 조회 / 수정 / 삭제
class ScheduleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(user=user)

    # DELETE 요청
    def delete(self, request, *args, **kwargs):
        schedule = self.get_object()
        schedule.delete()
        return Response({"data": {"message": "Schedule deleted"}}, status=status.HTTP_200_OK)
