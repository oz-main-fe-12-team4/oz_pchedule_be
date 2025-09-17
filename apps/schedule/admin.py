from django.contrib import admin
from .models import Schedule, Recurrence


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "start_time", "end_time", "is_completed", "created_at")
    list_filter = ("is_completed", "start_time", "end_time")
    search_fields = ("title", "user__email")
    ordering = ("-created_at",)


@admin.register(Recurrence)
class RecurrenceAdmin(admin.ModelAdmin):
    list_display = ("id", "schedule", "recurrence_type", "interval", "end_date")
    list_filter = ("recurrence_type",)
    search_fields = ("schedule__title",)
    ordering = ("-id",)
