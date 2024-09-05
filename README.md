# 썸닥터 (SomeDoctor)

사용자의 카카오톡 대화를 분석하여 썸 관계를 진단해주는 웹 어플리케이션입니다.

## 설치 및 실행 방법

### 프론트엔드 (Next.js)

Next.js로 부트스트랩된 프로젝트입니다. 개발 서버를 실행하려면 아래 명령어를 사용하세요:

```bash
npm run dev
# 또는
yarn dev
# 또는
pnpm dev
# 또는
bun dev
```

브라우저에서 [http://localhost:3000](http://localhost:3000) 링크를 열어 결과를 확인할 수 있습니다.

`app/page.tsx` 파일을 수정하여 페이지를 편집할 수 있으며, 수정하면 페이지가 자동으로 업데이트됩니다.

이 프로젝트는 [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts)를 사용하여 Vercel의 새로운 폰트 패밀리인 [Geist](https://vercel.com/font)를 최적화하고 로드합니다.

더 많은 정보는 [Next.js 문서](https://nextjs.org/docs)를 참조하세요.

### 배포 (Vercel)

Next.js 애플리케이션을 배포하는 가장 쉬운 방법은 Next.js의 제작자인 Vercel 플랫폼을 사용하는 것입니다. 자세한 내용은 [Next.js 배포 문서](https://nextjs.org/docs/app/building-your-application/deploying)를 확인하세요.

### 백엔드 (Flask)

1. 프로젝트 디렉토리로 이동하여 가상 환경을 활성화합니다.
2. 필요한 패키지를 설치합니다:

### **1. 가상 환경(venv) 설정 방법**

가상 환경을 사용하면 프로젝트의 의존성을 격리할 수 있어 다른 프로젝트와 충돌을 방지할 수 있습니다. 다음은 가상 환경을 설정하고 `requirements.txt`에 있는 패키지를 설치하는 방법입니다.

1. **가상 환경 생성 및 활성화**
   ```bash
   # 가상 환경 생성
   python3 -m venv venv

   # 가상 환경 활성화 (Windows)
   venv\Scripts\activate

   # 가상 환경 활성화 (Mac/Linux)
   source venv/bin/activate
   ```

2. **필요한 패키지 설치**
   ```bash
   # 가상 환경 활성화 후, 의존성 설치
   pip install -r requirements.txt
   ```

3. **가상 환경 비활성화**
   ```bash
   deactivate
   ```

위의 단계를 따라 프론트엔드와 백엔드를 설정하고 실행할 수 있습니다. 

---