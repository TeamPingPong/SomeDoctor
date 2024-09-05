# SomeDoctor
사용자의 카카오톡 내용을 분석해서 이를 수치화시켜 썸의 관계를 진단해주는 어플(웹)

## 설치 및 실행 방법

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