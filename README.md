# AI 프롬프트 생성기

이미지를 분석해서 Midjourney, DALL-E 같은 AI 이미지 생성 도구용 고품질 프롬프트를 자동으로 만들어주는 도구

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 특징

- 완전 무료 (Google Gemini 1.5 Flash)
- 빠른 생성 (1-3초)
- 고품질 영문 프롬프트
- 간단한 GUI
- 로컬 실행 (서버 불필요)

---

## 빠른 시작

### 1단계: API Key 발급 (무료)

1. https://aistudio.google.com/app/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭
4. API Key 복사

### 2단계: 설치

```bash
# 저장소 클론
git clone https://github.com/RiaLeee/prompt-from-image.git
cd prompt-from-image

# 패키지 설치
pip install -r requirements.txt

# API Key 설정
copy .env.example .env
# .env 파일을 열어서 API Key 입력
```

### 3단계: 실행

```bash
python src/promptmaker_gui.py
```

---

## 사용 방법

### 간단한 3단계

1. **이미지 선택** → 참고할 이미지 업로드 (1-2장)
2. **텍스트 입력** → 원하는 스타일/장면 설명 입력
   - 예: "두 양갈래 소녀들이 하이파이브하는 지브리 스타일"
3. **생성 & 복사** → 프롬프트 생성 후 복사 버튼 클릭

### 결과 사용

생성된 프롬프트를 Midjourney, DALL-E, Stable Diffusion 등에 바로 붙여넣기!

---

## 예시

**입력**
- 이미지: 애니메이션 캐릭터 이미지
- 텍스트: "두 양갈래 소녀들이 하이파이브하는 지브리 스타일"

**출력**
```
Modern high-budget 3D animated feature film style, Disney/Pixar
aesthetic, high-fidelity CGI render. Studio Ghibli inspired art
direction with soft watercolor backgrounds. A medium shot,
front-facing view of two cheerful girls with twin-tail hairstyles
doing high-five gesture...
```

---

## EXE 파일로 배포

Python 없이 실행 가능한 프로그램 만들기:

```bash
python scripts/build_exe.py
```

생성된 `release/prompt-maker-v1.0/` 폴더를 ZIP으로 압축하여 배포

자세한 내용: [docs/BUILD.md](docs/BUILD.md)

---

## 프로젝트 구조

```
prompt-from-image/
├── src/                    # 소스 코드
│   ├── promptmaker_gui.py  # 메인 GUI
│   └── gemini_api.py       # API 모듈
├── docs/                   # 문서
├── scripts/                # 빌드 스크립트
├── requirements.txt
└── .env.example
```

---

## 자주 묻는 질문

**Q. API Key를 어떻게 발급받나요?**
- https://aistudio.google.com/app/apikey 에서 무료로 발급 (하루 1,500회 사용 가능)

**Q. 프롬프트가 영어로만 나와요**
- 정상입니다. AI 이미지 생성 도구는 영어 프롬프트가 더 정확합니다

**Q. API 연결 실패 오류가 나요**
- API Key 확인, 인터넷 연결 확인, 일일 사용 횟수 확인

**Q. conda 명령어가 안 돼요**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

## 비용

완전 무료! (Google Gemini 1.5 Flash 무료 버전 사용)

---

## 보안 주의

- `.env` 파일에 API Key가 저장되니 절대 공유하지 마세요
- `.gitignore`에 자동으로 제외되어 있습니다

---

## 라이선스

MIT License

---

## 기여

이슈 및 PR 환영합니다!

- GitHub: https://github.com/RiaLeee/prompt-from-image

---

버전: 1.0
