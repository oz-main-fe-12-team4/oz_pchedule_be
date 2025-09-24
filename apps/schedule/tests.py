from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Schedule, DetailSchedule
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class ScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@test.com", password="1234")
        self.category = Category.objects.create(name="일상")

    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            user=self.user,
            title="테스트 일정",
            start_period=timezone.now(),
            end_period=timezone.now() + timedelta(hours=1),
            category=self.category,
        )
        self.assertEqual(schedule.title, "테스트 일정")
        self.assertFalse(schedule.is_deleted)

    def test_detail_schedule_creation(self):
        schedule = Schedule.objects.create(
            user=self.user,
            title="테스트 일정",
            start_period=timezone.now(),
            end_period=timezone.now() + timedelta(hours=1),
            category=self.category,
        )
        detail = DetailSchedule.objects.create(
            schedule=schedule,
            title="세부 일정",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(minutes=30),
        )
        self.assertEqual(detail.schedule, schedule)
        self.assertFalse(detail.is_completed)
