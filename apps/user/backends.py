from django.contrib.auth.backends import ModelBackend
from .models import User


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        print(f"🔥 CustomBackend called! username={username}, email={email}, password={password}")

        # username 파라미터를 email로 사용 (Django 기본 방식)
        if email is None:
            email = username

        if not email:
            return None

        print(f"🔍 Looking for user with email: {email}")
        try:
            user = User.objects.get(email=email)
            print(f"✅ User found: {user.email}")
            password_check = user.check_password(password)
            print(f"🔐 Password check: {password_check}")

            if password_check and self.user_can_authenticate(user):
                return user
        except User.DoesNotExist:
            print("❌ User not found")
        return None
