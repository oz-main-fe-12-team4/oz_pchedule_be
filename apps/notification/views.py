from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, permissions
from rest_framework.response import Response
from .models import Notification


class NotificationListAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # 로그인한 유저의 알림만 가져오기, 읽지 않은 알림 우선, 그다음 최신순
        notifications = Notification.objects.filter(user=request.user, is_deleted=False).order_by(
            "is_read", "-created_at"
        )
        serializer = self.get_serializer(notifications, many=True)
        return Response({"data": serializer.data})


class NotificationReadAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id, *args, **kwargs):
        # 특정 알림 가져오기
        notification = get_object_or_404(Notification, id=notification_id, user=request.user, is_deleted=False)

        # 읽음 처리
        notification.is_read = True
        notification.save()

        return Response({"message": "알림이 읽음 처리되었습니다."}, status=status.HTTP_200_OK)


class NotificationDeleteAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, notification_id, *args, **kwargs):
        # 특정 알림 가져오기
        notification = get_object_or_404(Notification, id=notification_id, user=request.user, is_deleted=False)

        # 삭제 처리 (is_deleted 필드 업데이트)
        notification.is_deleted = True
        notification.save()

        return Response({"message": "알림이 삭제되었습니다."}, status=status.HTTP_200_OK)
