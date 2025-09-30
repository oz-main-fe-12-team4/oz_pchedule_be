from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Schedule, Category, DetailSchedule, RecurrenceRule, Weekday

User = get_user_model()


class ScheduleAPITestCase(APITestCase):
    def setUp(self):
        # 사용자 생성 및 로그인
        self.user = User.objects.create_user(email="test@example.com", password="testpass")
        self.client.force_authenticate(user=self.user)

        self.other_user = User.objects.create_user(email="other@example.com", password="otherpass")

        # 카테고리 생성
        self.category = Category.objects.create(name="테스트 카테고리")

        # 요일 생성 (월~금)
        self.weekdays = [
            Weekday.objects.create(code=str(i), name=name) for i, name in enumerate(["월", "화", "수", "목", "금"], 1)
        ]

        # 테스트 일정 생성
        self.schedule = Schedule.objects.create(
            user=self.user,
            title="테스트 일정",
            start_period="2025-10-01T10:00:00Z",
            end_period="2025-10-01T12:00:00Z",
            category=self.category,
            priority="중간",
            share_type="비공개",
        )

    # ------------------- 일정 리스트 조회 -------------------
    def test_schedule_list(self):
        url = reverse("schedule-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()["data"]
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "테스트 일정")

    # ------------------- 일정 생성 -------------------
    def test_schedule_create(self):
        url = reverse("schedule-create")
        payload = {
            "title": "새로운 일정",
            "start_period": "2025-11-01T10:00:00Z",
            "end_period": "2025-11-01T12:00:00Z",
            "category": self.category.id,
            "priority": "높음",
            "share_type": "전체공개",
            "is_someday": False,
            "detail_schedule": [
                {
                    "title": "세부 일정1",
                    "description": "세부 내용",
                    "start_time": "2025-11-01T10:00:00Z",
                    "end_time": "2025-11-01T11:00:00Z",
                    "is_completed": False,
                }
            ],
            "recurrence_rule": {"frequency": "DAILY", "interval": 1, "weekdays": [wd.id for wd in self.weekdays]},
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Schedule 객체 확인
        new_schedule = Schedule.objects.get(title="새로운 일정")
        self.assertEqual(new_schedule.detail_schedule.count(), 1)
        self.assertTrue(hasattr(new_schedule, "recurrence_rule"))

        # ------------------- DetailSchedule 직접 검증 -------------------
        detail = new_schedule.detail_schedule.first()
        self.assertIsInstance(detail, DetailSchedule)
        self.assertEqual(detail.title, "세부 일정1")

        # ------------------- RecurrenceRule 직접 검증 -------------------
        rule = new_schedule.recurrence_rule
        self.assertIsInstance(rule, RecurrenceRule)
        self.assertEqual(rule.frequency, "DAILY")
        self.assertEqual(rule.weekdays.count(), 5)

    # ------------------- 일정 상세 조회 -------------------
    def test_schedule_detail(self):
        url = reverse("schedule-detail", kwargs={"pk": self.schedule.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["title"], "테스트 일정")

    # ------------------- 일정 수정 -------------------
    def test_schedule_update(self):
        url = reverse("schedule-detail", kwargs={"pk": self.schedule.id})
        payload = {"title": "수정된 일정"}
        response = self.client.put(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.schedule.refresh_from_db()
        self.assertEqual(self.schedule.title, "수정된 일정")

    # ------------------- 일정 삭제 -------------------
    def test_schedule_delete(self):
        url = reverse("schedule-detail", kwargs={"pk": self.schedule.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Schedule.objects.filter(id=self.schedule.id).exists())

    # ------------------- 다른 유저 일정 접근 -------------------
    def test_schedule_detail_other_user(self):
        other_schedule = Schedule.objects.create(user=self.other_user, title="다른 유저 일정")
        url = reverse("schedule-detail", kwargs={"pk": other_schedule.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
