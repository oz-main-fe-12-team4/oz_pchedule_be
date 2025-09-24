from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Schedule, DetailSchedule
from .serializers import ScheduleSerializer, DetailScheduleSerializer


class ScheduleListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get(self, request):
        schedules = Schedule.objects.filter(user=request.user, is_deleted=False)
        serializer = self.get_serializer(schedules, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 겹치는 일정 체크
        start = serializer.validated_data["start_period"]
        end = serializer.validated_data["end_period"]
        overlap = Schedule.objects.filter(
            user=request.user, is_deleted=False, start_period__lt=end, end_period__gt=start
        ).exists()
        if overlap:
            return Response({"error": "겹치는 일정이 존재합니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(user=request.user)
        return Response({"message": "일정이 생성되었습니다."}, status=status.HTTP_201_CREATED)


class ScheduleDetailAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_object(self, schedule_id):
        return generics.get_object_or_404(Schedule, id=schedule_id, user=self.request.user, is_deleted=False)

    def get(self, request, schedule_id):
        schedule = self.get_object(schedule_id)
        serializer = self.get_serializer(schedule)
        return Response({"data": serializer.data})

    def put(self, request, schedule_id):
        schedule = self.get_object(schedule_id)
        serializer = self.get_serializer(schedule, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "일정이 수정되었습니다."})

    def delete(self, request, schedule_id):
        schedule = self.get_object(schedule_id)
        schedule.is_deleted = True
        schedule.save()
        return Response({"message": "게시물이 삭제되었습니다."}, status=status.HTTP_200_OK)


class DetailScheduleCompleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, detail_id):
        detail = generics.get_object_or_404(DetailSchedule, id=detail_id, schedule__user=request.user)
        detail.is_completed = True
        detail.save()
        return Response({"message": "일정이 완료되었습니다."})


class DetailScheduleUpdateDeleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DetailScheduleSerializer

    def get_object(self, detail_id):
        return generics.get_object_or_404(DetailSchedule, id=detail_id, schedule__user=self.request.user)

    def put(self, request, detail_id):
        detail = self.get_object(detail_id)
        serializer = self.get_serializer(detail, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "일정이 수정되었습니다."})

    def delete(self, request, detail_id):
        detail = self.get_object(detail_id)
        detail.delete()
        return Response({"message": "일정이 삭제되었습니다."})
