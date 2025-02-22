### 개요
nsfw  Image classify
(AI Model활용 부적절 이미지 판정)
- 백엔드 서비스: FastApi (Python)
- 프론트 : Vue

### 사용법
Image를 업로드시 부적합 여부를 AI 모델에 의해 판단 결과 조회됨


![Drop zone output](./dnd.gif)

### 프로그램 구성도


![Drop zone output](./dnd.gif)

### FrontEnd 설정 
- .env 파일에 백엔드 서비스 url 입력
  예) VUE_APP_API_URL=http://xxxxxx:8001

 
- 모듈 설치

```bash
npm install
# OR
yarn install
```

- 컴파일 및 서버 실행 
```bash
npm run serve
# OR
yarn serve
```
- 웹서버에 배포시 빌드
```bash
npm run build
# ORD
yarn build
```
- 규칙에 맞도록 소스 보완 시 사용 
```
yarn lint
```

### 참고한 소스 
AI Detect Model : https://github.com/GantMan/nsfw_model.git
