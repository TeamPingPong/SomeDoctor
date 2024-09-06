# 빌드 단계
FROM node:18-slim AS builder

# 작업 디렉터리 생성
WORKDIR /app

# package.json 및 package-lock.json 파일 복사
COPY package.json package-lock.json ./

# 의존성 설치
RUN npm ci

# 애플리케이션 소스 복사
COPY . .

# 프로덕션 빌드
RUN npm run build

# 실제 실행 단계
FROM node:18-slim

# 작업 디렉터리 생성
WORKDIR /app

# 빌드된 파일만 복사
COPY --from=builder /app ./

# 서버 실행
CMD ["npm", "run", "start"]
