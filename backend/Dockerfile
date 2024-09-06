# Python 3.12 slim 버전 사용
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사
COPY requirements.txt requirements.txt

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 5000 포트 노출
EXPOSE 5000

# 애플리케이션 실행
CMD ["python", "run.py", "--host=0.0.0.0"]
