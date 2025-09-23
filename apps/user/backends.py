from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        print("🔥 CustomBackend called!", email, password)
        # 디버깅
        if email is None:
            email = kwargs.get("username")  # fallback
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        print("check_password:", user.check_password(password))
        print("is_active:", user.is_active)
        return None
