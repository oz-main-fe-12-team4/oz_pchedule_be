from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.hashers import check_password
from apps.user.models import User


class UserAPITestCase(APITestCase):
    def setUp(self):
        # 테스트용 유저 생성
        self.user = User.objects.create_user(email="test@example.com", password="testpass", name="TestUser")
        self.admin_user = User.objects.create_user(
            email="admin@example.com", password="adminpass", name="AdminUser", is_admin=True
        )

    # ------------------- 회원가입 -------------------
    def test_signup(self):
        url = reverse("user-signup")
        payload = {"email": "newuser@example.com", "password": "newpass123", "name": "NewUser"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    # ------------------- 로그인 -------------------
    def test_login(self):
        url = reverse("user-login")
        payload = {"email": "test@example.com", "password": "testpass"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    # ------------------- 내 정보 조회 -------------------
    def test_user_info(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-info")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["data"]["email"], self.user.email)

    # ------------------- 이름 변경 -------------------
    def test_change_name(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-name-update")
        payload = {"name": "UpdatedName"}
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, "UpdatedName")

    # ------------------- 비밀번호 변경 -------------------
    def test_change_password(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-password-change")
        payload = {"current_password": "testpass", "new_password": "newpassword", "new_password_confirm": "newpassword"}
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(check_password("newpassword", self.user.password))

    # ------------------- 회원 탈퇴 -------------------
    def test_user_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("user-delete")
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(User.objects.filter(email="test@example.com").exists())

    # ------------------- 관리자 유저 리스트 조회 -------------------
    def test_admin_user_list(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("admin-user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("summary", response.json())
        self.assertIn("users", response.json())

    # ------------------- 관리자 계정 활성화/비활성화 -------------------
    def test_admin_activate_deactivate_user(self):
        self.client.force_authenticate(user=self.admin_user)
        # 비활성화
        url_deactivate = reverse("admin-user-deactivate", kwargs={"user_id": self.user.id})
        response = self.client.post(url_deactivate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)
        # 활성화
        url_activate = reverse("admin-user-activate", kwargs={"user_id": self.user.id})
        response = self.client.post(url_activate)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
