from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Schedule, Recurrence
from apps.post.models import Post
from apps.post.serializers import ScheduleSerializer, RecurrenceSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    serializer_class = ScheduleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(post__user=self.request.user)

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        post = Post.objects.get(id=post_id, user=self.request.user)
        serializer.save(post=post)


class RecurrenceViewSet(viewsets.ModelViewSet):
    serializer_class = RecurrenceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Recurrence.objects.filter(post__user=self.request.user)

    def perform_create(self, serializer):
        post_id = self.request.data.get("post")
        post = Post.objects.get(id=post_id, user=self.request.user)
        serializer.save(post=post)
