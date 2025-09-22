from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class NotificationAPITest(APITestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.other_user = User.objects.create_user(username="otheruser", password="password123")

        # 테스트용 알림 생성
        self.notification1 = Notification.objects.create(user=self.user, content="알림1")
        self.notification2 = Notification.objects.create(user=self.user, content="알림2", is_read=True)
        self.notification_other = Notification.objects.create(user=self.other_user, content="다른 유저 알림")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_notification_list(self):
        url = "/notifications/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 로그인한 유저 알림만 반환
        self.assertEqual(len(response.data["data"]), 2)
        # 읽지 않은 알림이 먼저 나오는지 확인
        self.assertFalse(response.data["data"][0]["is_read"])

    def test_notification_read(self):
        url = f"/notifications/{self.notification1.id}/read/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Notification.objects.get(id=self.notification1.id).is_read)

    def test_notification_read_permission_denied(self):
        url = f"/notifications/{self.notification_other.id}/read/"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("권한", response.data["error"])

    def test_notification_delete(self):
        url = f"/notifications/{self.notification1.id}/delete/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(id=self.notification1.id).exists())

    def test_notification_delete_permission_denied(self):
        url = f"/notifications/{self.notification_other.id}/delete/"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("권한", response.data["error"])
