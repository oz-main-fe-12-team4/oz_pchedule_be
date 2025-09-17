from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from datetime import datetime


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="tester")
        self.post = Post.objects.create(
            user=self.user,
            title="테스트 일정",
            start_period=datetime(2025, 1, 1, 10, 0),
            end_period=datetime(2025, 1, 1, 12, 0),
            is_someday=False,
        )

    def test_post_creation(self):
        """Post가 정상적으로 생성되는지 확인"""
        self.assertEqual(self.post.title, "테스트 일정")
        self.assertEqual(self.post.user.username, "tester")

    def test_post_str(self):
        """__str__ 메서드가 title을 반환하는지 확인"""
        self.assertEqual(str(self.post), self.post.title)
