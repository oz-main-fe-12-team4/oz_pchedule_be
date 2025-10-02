from dotenv import load_dotenv
from .base import *
import os

DEBUG = False

# .env 로드
load_dotenv(BASE_DIR / ".env")  # noqa: F405

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "").split(",")

# Django 4.0+에서는 반드시 스킴 포함 (https:// ...)
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
CORS_ALLOW_CREDENTIALS = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

# -------------------------------
# CSRF / SESSION 쿠키 설정 (prod 전용)
# -------------------------------

# CSRF 쿠키: HTTPS + cross-site 요청 가능 + JS 접근 가능
CSRF_COOKIE_SECURE = True  # HTTPS에서만 전송
CSRF_COOKIE_SAMESITE = "None"  # cross-site 허용
CSRF_COOKIE_HTTPONLY = False  # JS에서 읽어서 X-CSRFToken 헤더에 넣기 위해 False

# 세션 쿠키도 동일 정책
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = "None"
SESSION_COOKIE_HTTPONLY = True  # 세션 쿠키는 JS 접근 불가(보안상 안전)
