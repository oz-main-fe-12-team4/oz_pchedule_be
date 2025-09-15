# 베이스 이미지
FROM python:3.13-slim

# 환경 변수
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"

# 필수 패키지 설치
RUN apt-get update && apt-get install -y curl build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# uv 설치
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# 작업 디렉토리
WORKDIR /app

# 코드 복사
COPY . .

# 의존성 설치
RUN uv pip install --system .[dev]

# 실행 스크립트 권한
RUN chmod +x /app/scripts/run.sh

# 포트 노출
EXPOSE 8000

# 컨테이너 시작 시 run.sh 실행
CMD ["/app/scripts/run.sh"]