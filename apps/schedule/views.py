from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from .models import Category, Schedule, DetailSchedule, Recurrence, Weekday
from .serializers import (
    CategorySerializer,
    ScheduleSerializer,
    DetailScheduleSerializer,
    RecurrenceSerializer,
    WeekdaySerializer,
)


# --- Category ---
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    http_method_names = ["get", "post", "delete"]  # PUT, PATCH 제거


# --- Weekday ---
class WeekdayViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Weekday.objects.all()
    serializer_class = WeekdaySerializer


# --- Schedule ---
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().select_related("category", "user")
    serializer_class = ScheduleSerializer
    http_method_names = ["get", "post", "delete"]


# --- DetailSchedule ---
class DetailScheduleViewSet(viewsets.ModelViewSet):
    queryset = DetailSchedule.objects.all().select_related("schedule")
    serializer_class = DetailScheduleSerializer
    http_method_names = ["get", "post", "delete"]

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        """
        상세 일정 완료 처리
        """
        detail = self.get_object()
        detail.is_completed = True
        detail.completed_at = timezone.now()
        detail.save()
        return Response({"is_completed": detail.is_completed, "completed_at": detail.completed_at})


# --- Recurrence ---
class RecurrenceViewSet(viewsets.ModelViewSet):
    queryset = Recurrence.objects.all().select_related("schedule")
    serializer_class = RecurrenceSerializer
    http_method_names = ["get", "post", "delete"]
