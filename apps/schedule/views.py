from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Schedule, DetailSchedule
from .serializers import ScheduleSerializer, DetailScheduleSerializer


# ----------------------
# Schedule
# ----------------------
class ScheduleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(user=user)

    def perform_create(self, serializer):
        # 생성 시 현재 사용자로 설정
        serializer.save(user=self.request.user)


class ScheduleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "delete"]  # PATCH 제거, PUT만 허용

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.all()
        return Schedule.objects.filter(user=user)

    # PUT을 부분 업데이트처럼 허용(편의). 필요하면 전체 갱신으로 바꿀 수 있음.
    def update(self, request, *args, **kwargs):
        partial = True  # PUT을 부분 업데이트로 처리 (PATCH 사용 안하므로)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


# ----------------------
# DetailSchedule
# ----------------------
class DetailScheduleListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DetailScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 자신(유저)의 스케줄들에 속한 detail만 조회
        return DetailSchedule.objects.filter(schedule__user=user)

    def perform_create(self, serializer):
        # 생성 시 전달된 schedule이 현재 유저의 소유인지 확인
        schedule = serializer.validated_data.get("schedule")
        if schedule is None:
            raise PermissionDenied("schedule 필드가 필요합니다.")
        if schedule.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("해당 스케줄에 대한 권한이 없습니다.")
        serializer.save()


class DetailScheduleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailScheduleSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "delete"]  # PATCH 제거, PUT만 허용

    def get_queryset(self):
        user = self.request.user
        return DetailSchedule.objects.filter(schedule__user=user)

    # PUT을 부분 업데이트처럼 허용 -> is_completed만 보내 토글 가능
    def update(self, request, *args, **kwargs):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
