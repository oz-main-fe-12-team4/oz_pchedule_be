from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Schedule, DetailSchedule
from django.utils import timezone
from datetime import timedelta


User = get_user_model()


class ScheduleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.category = Category.objects.create(name="일상")

    def test_schedule_creation(self):
        schedule = Schedule.objects.create(
            user=self.user,
            title="Test Schedule",
            category=self.category,
            start_period=timezone.now(),
            end_period=timezone.now() + timedelta(hours=1),
        )
        self.assertEqual(schedule.title, "Test Schedule")

    def test_detail_schedule_within_period(self):
        schedule = Schedule.objects.create(
            user=self.user,
            title="Main Schedule",
            category=self.category,
            start_period=timezone.now(),
            end_period=timezone.now() + timedelta(days=1),
        )
        detail = DetailSchedule.objects.create(
            schedule=schedule,
            title="Detail Task",
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
        )
        self.assertFalse(detail.is_completed)
