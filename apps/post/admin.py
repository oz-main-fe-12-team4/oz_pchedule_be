from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "start_period", "end_period", "is_someday")
    search_fields = ("title", "user__username")
    list_filter = ("is_someday", "start_period")
    ordering = ("-id",)
