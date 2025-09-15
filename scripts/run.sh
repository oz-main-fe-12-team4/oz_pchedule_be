#!/bin/bash
# 데이터베이스 준비
python manage.py migrate

# 개발 서버 실행
uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload