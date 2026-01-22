FROM python:3.11-slim
WORKDIR /app

# CI에서 설치한 패키지를 그대로 사용하려면, 패키지를 포함한 폴더를 복사
# 예: site-packages를 포함한 wheel 또는 install 폴더를 COPY
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]