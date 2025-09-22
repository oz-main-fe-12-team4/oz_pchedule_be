from django.urls import path

from apps.notification.views import NotificationListAPIView, NotificationReadAPIView, NotificationDeleteAPIView

urlpatterns = [
    path("", NotificationListAPIView.as_view(), name="notification-list"),
    path("<int:pk>/read/", NotificationReadAPIView.as_view(), name="notification-read"),
    path("<int:pk>/", NotificationDeleteAPIView.as_view(), name="notification-delete"),
]
