from django.urls import path

from apps.notification.views import NotificationListAPIView, NotificationReadAPIView, NotificationDeleteAPIView

urlpatterns = [
    path("list/", NotificationListAPIView.as_view(), name="notification-list"),
    path("read/", NotificationReadAPIView.as_view(), name="notification-read"),
    path("delete/", NotificationDeleteAPIView.as_view(), name="notification-delete"),
]
