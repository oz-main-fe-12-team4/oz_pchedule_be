from rest_framework import viewsets
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


class RecurrenceViewSet(viewsets.ModelViewSet):
    queryset = Recurrence.objects.all().select_related("schedule")
    serializer_class = RecurrenceSerializer
