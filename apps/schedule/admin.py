from django.contrib import admin
from .models import Category, Schedule, DetailSchedule, Recurrence, Weekday


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "user", "priority", "share_type", "created_at"]
    list_filter = ["priority", "share_type", "category"]


@admin.register(DetailSchedule)
class DetailScheduleAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "schedule", "is_completed", "start_time", "end_time"]


@admin.register(Recurrence)
class RecurrenceAdmin(admin.ModelAdmin):
    list_display = ["id", "schedule", "type", "until"]


@admin.register(Weekday)
class WeekdayAdmin(admin.ModelAdmin):
    list_display = ["id"]
