from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.schedule.models import Schedule
from .models import Like, Bookmark, Report

User = get_user_model()


class InteractionsAPITestCase(APITestCase):
    def setUp(self):
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)

        # 테스트용 일정 생성
        self.schedule = Schedule.objects.create(
            user=self.user,
            title="테스트 일정",
            start_period="2025-10-01T10:00:00Z",
            end_period="2025-10-01T12:00:00Z",
        )

    # ------------------- Like -------------------
    def test_like_schedule(self):
        url = reverse("like") + f"?schedule_id={self.schedule.id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Like.objects.filter(user=self.user, schedule=self.schedule).exists())

    def test_unlike_schedule(self):
        # 먼저 좋아요 생성
        Like.objects.create(user=self.user, schedule=self.schedule)
        url = reverse("like") + f"?schedule_id={self.schedule.id}"
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Like.objects.filter(user=self.user, schedule=self.schedule).exists())

    # ------------------- Bookmark -------------------
    def test_bookmark_schedule(self):
        url = reverse("bookmark") + f"?schedule_id={self.schedule.id}"
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Bookmark.objects.filter(user=self.user, schedule=self.schedule).exists())

    # ------------------- Report -------------------
    def test_report_schedule(self):
        url = reverse("report") + f"?schedule_id={self.schedule.id}"
        data = {"reason": Report.REASONS[0][0]}  # 첫 번째 신고 사유 선택
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Report.objects.filter(user=self.user, schedule=self.schedule).exists())

    def test_report_schedule_already_reported(self):
        # 먼저 신고 생성
        Report.objects.create(user=self.user, schedule=self.schedule, reason=Report.REASONS[0][0])
        url = reverse("report") + f"?schedule_id={self.schedule.id}"
        data = {"reason": Report.REASONS[0][0]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
