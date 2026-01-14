# 🎨 AI 프롬프트 생성기

이미지와 텍스트를 입력하면 AI가 자동으로 고품질 이미지 생성 프롬프트를 만들어주는 **Python GUI 데스크톱 애플리케이션**

![Version](https://img.shields.io/badge/version-1.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## 📋 목차

- [소개](#소개)
- [주요 기능](#주요-기능)
- [사전 준비](#사전-준비)
- [설치 방법](#설치-방법)
- [사용 방법](#사용-방법)
- [프로젝트 구조](#프로젝트-구조)
- [FAQ](#faq)

---

## 💡 소개

**Prompt From Image**는 Midjourney, DALL-E, Stable Diffusion 등 AI 이미지 생성 도구에 사용할 전문적인 프롬프트를 자동으로 생성해주는 도구입니다.

### 🎯 특징

- ✅ **완전 무료** (Google Gemini 1.5 Flash 사용)
- ✅ **간단한 GUI** (Tkinter 기반)
- ✅ **개인용 로컬 실행** (서버 불필요)
- ✅ **빠른 응답** (1-3초 내 생성)
- ✅ **고품질 프롬프트** (전문가 수준의 영문 프롬프트)

---

## ⚡ 주요 기능

### 1. 이미지 분석
- 1~2장의 참고 이미지 업로드
- AI가 색감, 조명, 구도, 스타일 자동 분석

### 2. 프롬프트 생성
- 사용자 텍스트 + 이미지 분석 결과 통합
- JSON 형식의 구조화된 프롬프트 생성
  - `style_prompt`: 스타일 중심 프롬프트
  - `scene_prompt`: 장면 중심 프롬프트
  - `final_prompt`: 최종 통합 프롬프트 (바로 사용 가능)

### 3. 결과 활용
- 📋 클립보드 복사 (원클릭)
- 💾 JSON 파일 저장
- 🚀 Midjourney, DALL-E 등에 바로 사용

---

## 🛠️ 사전 준비

### 1. Python 설치
- Python 3.10 이상 필요
- [Python 다운로드](https://www.python.org/downloads/)

### 2. Miniconda 설치 (권장)
- [Miniconda 다운로드](https://docs.conda.io/en/latest/miniconda.html)

### 3. Gemini API Key 발급
1. [Google AI Studio](https://aistudio.google.com/app/apikey) 접속
2. Google 계정 로그인
3. **"Create API Key"** 클릭
4. API Key 복사 및 저장

> 📌 **완전 무료** (일일 1,500 요청 제한)

자세한 가이드: [docs/SETUP.md](docs/SETUP.md) 참고

---

## 📦 설치 방법

### 1. 저장소 클론 또는 다운로드

```bash
# Git 클론
git clone https://github.com/your-username/prompt-from-image.git
cd prompt-from-image

# 또는 ZIP 다운로드 후 압축 해제
```

### 2. 가상환경 생성 (Conda)

```bash
# 'ai'라는 이름으로 가상환경 생성
conda create -n ai python=3.10 -y

# 가상환경 활성화
conda activate ai
```

### 3. 패키지 설치

```bash
pip install -r requirements.txt
```

### 4. API Key 설정

`.env` 파일 생성 (또는 `.env.example` 복사):

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

`.env` 파일 내용 수정:

```env
GEMINI_API_KEY=여기에_발급받은_API_Key_입력
```

---

## 🚀 사용 방법

### 1. 프로그램 실행

```bash
# 가상환경 활성화 (conda 사용 시)
conda activate ai

# GUI 프로그램 실행
python src/promptmaker_gui.py
```

### 2. GUI 사용

1. **📸 이미지 선택**
   - "파일 선택..." 버튼 클릭
   - JPG, PNG, WEBP 파일 선택 (최대 10MB)
   - 이미지 1은 필수, 이미지 2는 선택사항

2. **✍️ 텍스트 입력**
   - 원하는 스타일이나 장면 설명 입력
   - 예: "두 양갈래 소녀들이 하이파이브하고 있는 지브리 스타일로"

3. **🔑 API Key 입력**
   - .env 파일에 저장했다면 자동으로 로드됨
   - 직접 입력도 가능 (마스킹 처리됨)
   - "테스트" 버튼으로 연결 확인

4. **🚀 생성**
   - "프롬프트 생성하기" 버튼 클릭
   - 1-10초 대기 (AI 분석 중)
   - JSON 결과 표시

5. **📋 결과 사용**
   - "복사" 버튼: final_prompt 클립보드 복사
   - "JSON 저장" 버튼: 전체 결과 파일로 저장

### 3. 생성된 프롬프트 사용

```
복사한 프롬프트를 Midjourney, DALL-E, Stable Diffusion 등에 붙여넣기
```

---

## 📂 프로젝트 구조

```
prompt-from-image/
├── src/                        # 소스 코드
│   ├── promptmaker_gui.py      # 메인 GUI 애플리케이션
│   └── gemini_api.py           # Gemini API 연동 모듈
│
├── docs/                       # 문서
│   ├── README.md               # 사용 설명서
│   ├── SETUP.md                # 사전 준비 가이드
│   ├── BUILD.md                # 빌드 가이드
│   └── RELEASE.md              # 배포 가이드
│
├── scripts/                    # 빌드 스크립트
│   └── build_exe.py            # 자동 빌드 스크립트
│
├── output/                     # JSON 결과 저장 (자동 생성)
│
├── requirements.txt            # 패키지 의존성
├── .env                        # API Key 저장 (Git 제외)
├── .env.example                # 환경변수 예시
└── .gitignore                  # Git 제외 파일
```

---

## 🎁 EXE 파일로 배포하기

Python 없이 실행 가능한 독립 실행형 프로그램 만들기:

```bash
# 자동 빌드 스크립트 실행
python scripts/build_exe.py

# 결과: release/prompt-maker-v1.0/ 폴더 생성
# ZIP으로 압축하여 배포 가능
```

자세한 내용: [docs/BUILD.md](docs/BUILD.md)

---

## 📖 예시

### 입력

**이미지**: 애니메이션 스타일의 소녀 캐릭터 이미지

**텍스트**: "두 양갈래 소녀들이 하이파이브하고 있는 지브리 스타일로"

### 출력 (JSON)

```json
{
  "meta": {
    "version": "3.0",
    "engine": "gemini-1.5-flash",
    "generated_at": "2026-01-14T13:30:45Z"
  },
  "inputs": {
    "reference_images_count": 1,
    "user_scene_text": "두 양갈래 소녀들이 하이파이브하고 있는 지브리 스타일로"
  },
  "prompts": {
    "style_prompt": "Modern high-budget 3D animated feature film style...",
    "scene_prompt": "A medium shot, front-facing view of two cheerful girls...",
    "final_prompt": "Modern high-budget 3D animated feature film style, Disney/Pixar aesthetic, high-fidelity CGI render. Studio Ghibli inspired art direction with soft watercolor backgrounds..."
  }
}
```

**`final_prompt`를 복사하여 AI 이미지 생성 도구에 사용!**

---

## ❓ FAQ

### Q1. API Key를 잃어버렸어요
**A**: Google AI Studio에서 기존 키를 삭제하고 새로 발급받으세요.

### Q2. "API 연결 실패" 오류가 나요
**A**:
1. API Key가 올바른지 확인
2. 인터넷 연결 확인
3. 일일 요청 제한(1,500회) 초과 여부 확인

### Q3. 이미지가 너무 크다고 나와요
**A**: 이미지를 10MB 이하로 리사이즈하거나 압축하세요.

### Q4. conda 명령어가 안 돼요
**A**: Miniconda를 설치하거나, Python venv 사용:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

### Q5. 프롬프트가 영어로만 나와요
**A**: 의도된 동작입니다. AI 이미지 생성 도구들은 영어 프롬프트를 권장합니다.

---

## 💰 비용

| 항목 | 비용 |
|------|------|
| Google Gemini 1.5 Flash | **무료** (1,500 요청/일) |
| Python & 라이브러리 | **무료** |
| **총 비용** | **$0 (영구 무료)** |

---

## 🔒 보안

- `.env` 파일은 절대 공개 저장소에 업로드 금지
- `.gitignore`에 자동으로 제외 처리됨
- API Key는 개인만 관리

---

## 📝 라이선스

MIT License

---

## 🤝 기여

이슈 및 풀 리퀘스트 환영합니다!

---

## 📞 문의

- GitHub Issues: [프로젝트 저장소](https://github.com/your-username/prompt-from-image/issues)

---

**작성일**: 2026-01-14
**버전**: 1.0
**개발**: Claude Code Assistant
