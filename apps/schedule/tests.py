from django.test import TestCase
from django.contrib.auth.models import User
from .models import Schedule
from datetime import datetime


class ScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester2")
        self.schedule = Schedule.objects.create(
            user=self.user,
            title="테스트 스케줄",
            start_period=datetime(2025, 1, 2, 14, 0),
            end_period=datetime(2025, 1, 2, 16, 0),
            is_someday=True,
        )

    def test_schedule_creation(self):
        """Schedule이 정상적으로 생성되는지 확인"""
        self.assertEqual(self.schedule.title, "테스트 스케줄")
        self.assertEqual(self.schedule.user.username, "tester2")

    def test_schedule_str(self):
        """__str__ 메서드가 title을 반환하는지 확인"""
        self.assertEqual(str(self.schedule), self.schedule.title)
