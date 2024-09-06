# Node.js 공식 이미지를 사용
FROM node:18

# 작업 디렉터리 생성
WORKDIR /app

# package.json 및 package-lock.json 파일을 복사
COPY package.json package-lock.json ./

# 의존성 설치
RUN npm install

# 애플리케이션 소스 복사
COPY . .

# 프로덕션 빌드
RUN npm run build

# 서버 실행
CMD ["npm", "run", "start"]
