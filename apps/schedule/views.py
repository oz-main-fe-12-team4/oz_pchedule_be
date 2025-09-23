from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Schedule, DetailSchedule, Recurrence, Weekday
from .serializers import (
    CategorySerializer,
    ScheduleSerializer,
    DetailScheduleSerializer,
    RecurrenceSerializer,
    WeekdaySerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class WeekdayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weekday.objects.all()
    serializer_class = WeekdaySerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().select_related("category", "user")
    serializer_class = ScheduleSerializer


class DetailScheduleViewSet(viewsets.ModelViewSet):
    queryset = DetailSchedule.objects.all().select_related("schedule")
    serializer_class = DetailScheduleSerializer

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        detail = self.get_object()
        detail.is_completed = True
        detail.save()
        return Response({"is_completed": detail.is_completed})


class RecurrenceViewSet(viewsets.ModelViewSet):
    queryset = Recurrence.objects.all().select_related("schedule")
    serializer_class = RecurrenceSerializer
