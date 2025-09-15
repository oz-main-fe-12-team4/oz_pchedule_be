from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=20, unique=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    allow_notification = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()


class LoginAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_attempt_time = models.DateTimeField(auto_now_add=True)
    is_success = models.BooleanField()
    ip_address = models.CharField(max_length=45)


class Token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    refresh_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_revoked = models.BooleanField(default=False)


class AccessTokenBlacklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=1024)
    revoked_at = models.DateTimeField(auto_now_add=True)
