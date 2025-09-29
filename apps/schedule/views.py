from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Schedule
from .serializers import ScheduleSerializer


class ScheduleListAPIView(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.filter(is_deleted=False)
        return Schedule.objects.filter(user=user, is_deleted=False)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class ScheduleCreateAPIView(generics.CreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)


class DetailScheduleUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Schedule.objects.filter(is_deleted=False)
        return Schedule.objects.filter(user=user, is_deleted=False)

    # 완료 토글 처리
    def patch(self, request, *args, **kwargs):
        schedule = self.get_object()
        if "toggle_complete" in request.data:
            schedule.is_complete = not schedule.is_complete  #
            schedule.save()
            return Response({"data": {"is_complete": schedule.is_complete}}, status=status.HTTP_200_OK)
        return self.partial_update(request, *args, **kwargs)
