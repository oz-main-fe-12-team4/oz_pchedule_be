from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Schedule, DetailSchedule
from .serializers import ScheduleSerializer, DetailScheduleSerializer


class ScheduleListCreateAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        qs = Schedule.objects.filter(is_deleted=False)
        user = self.request.user
        if not user.is_admin:
            qs = qs.filter(user=user)

        schedule_type = self.request.query_params.get("type")  # routine / someday / story
        if schedule_type == "routine":
            qs = qs.filter(is_recurrence=True)
        elif schedule_type == "someday":
            qs = qs.filter(is_someday=True)
        elif schedule_type == "story":
            qs = qs.filter(share_type="전체공개")
        return qs

    def get(self, request):
        schedules = self.get_queryset()
        serializer = self.get_serializer(schedules, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start = serializer.validated_data.get("start_period")
        end = serializer.validated_data.get("end_period")
        if start and end:
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
        user = self.request.user
        if user.is_admin:
            return generics.get_object_or_404(Schedule, id=schedule_id, is_deleted=False)
        return generics.get_object_or_404(Schedule, id=schedule_id, user=user, is_deleted=False)

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
        return Response({"message": "일정이 삭제되었습니다."}, status=status.HTTP_200_OK)


class DetailScheduleCompleteAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, detail_id):
        detail = generics.get_object_or_404(DetailSchedule, id=detail_id, schedule__user=request.user)
        detail.is_completed = True
        detail.save()
        return Response({"message": "세부 일정이 완료되었습니다."})


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
        return Response({"message": "세부 일정이 수정되었습니다."})

    def delete(self, request, detail_id):
        detail = self.get_object(detail_id)
        detail.delete()
        return Response({"message": "세부 일정이 삭제되었습니다."})
