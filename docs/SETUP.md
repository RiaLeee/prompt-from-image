# 🚀 사전 준비 가이드

프로젝트를 시작하기 전에 필요한 환경 설정 및 API 발급 방법을 안내합니다.

---

## 📋 목차

1. [미니콘다 가상환경 설정](#1-미니콘다-가상환경-설정)
2. [Gemini API Key 발급](#2-gemini-api-key-발급)
3. [필수 패키지 설치](#3-필수-패키지-설치)
4. [환경 변수 설정](#4-환경-변수-설정)
5. [설치 확인](#5-설치-확인)

---

## 1. 미니콘다 가상환경 설정

### 1.1 미니콘다 설치 여부 확인

```bash
conda --version
```

출력 예시: `conda 24.9.2`

만약 설치되어 있지 않다면, [Miniconda 공식 사이트](https://docs.conda.io/en/latest/miniconda.html)에서 다운로드하여 설치하세요.

### 1.2 가상환경 생성

```bash
# 'ai'라는 이름으로 Python 3.10 환경 생성
conda create -n ai python=3.10 -y
```

### 1.3 가상환경 확인

```bash
# 생성된 환경 목록 확인
conda env list
```

출력 결과에서 `ai` 환경이 보이면 성공입니다.

```
# conda environments:
#
base                     D:\Utility\miniconda3
ai                       D:\Utility\miniconda3\envs\ai
```

### 1.4 가상환경 활성화

**Windows (CMD):**
```bash
conda activate ai
```

**Windows (PowerShell):**
```powershell
conda activate ai
```

**Mac/Linux:**
```bash
conda activate ai
```

### 1.5 가상환경 비활성화

작업이 끝나면 다음 명령어로 환경을 비활성화할 수 있습니다.

```bash
conda deactivate
```

---

## 2. Gemini API Key 발급

Google의 Gemini API는 **완전 무료**로 사용할 수 있습니다 (일일 1,500 요청 제한).

### 2.1 Google AI Studio 접속

[Google AI Studio](https://aistudio.google.com/app/apikey)에 접속합니다.

> **직접 링크**: https://aistudio.google.com/app/apikey

### 2.2 Google 계정 로그인

- Google 계정으로 로그인합니다.
- 계정이 없다면 새로 생성해야 합니다.

### 2.3 API Key 생성

1. **"Get API Key"** 또는 **"Create API Key"** 버튼 클릭
2. 새 프로젝트를 생성하거나 기존 프로젝트 선택
   - 새 프로젝트 추천: **"Create API key in new project"** 선택
3. API Key가 생성되면 **복사** 버튼을 눌러 저장합니다.

```
예시: AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

⚠️ **중요**: API Key는 다시 확인할 수 없으므로 안전한 곳에 보관하세요!

### 2.4 API Key 보안 주의사항

- ❌ GitHub 등 공개 저장소에 업로드 금지
- ❌ 다른 사람과 공유 금지
- ✅ 환경 변수나 `.env` 파일에 저장 (아래 참고)

---

## 3. 필수 패키지 설치

가상환경이 활성화된 상태에서 아래 명령어를 실행합니다.

### 3.1 방법 1: 한 번에 설치

```bash
conda activate ai
pip install google-generativeai pillow pyperclip
```

### 3.2 방법 2: requirements.txt 사용

프로젝트에 `requirements.txt` 파일이 있다면:

```bash
conda activate ai
pip install -r requirements.txt
```

### 3.3 설치되는 패키지 설명

| 패키지 | 용도 | 버전 |
|--------|------|------|
| `google-generativeai` | Gemini API 연동 | 최신 |
| `pillow` | 이미지 파일 처리 | 최신 |
| `pyperclip` | 클립보드 복사 기능 | 최신 |

---

## 4. 환경 변수 설정

API Key를 안전하게 관리하기 위한 방법입니다.

### 4.1 `.env` 파일 생성

프로젝트 루트 디렉토리에 `.env` 파일을 생성합니다.

```bash
# 프로젝트 루트에서
touch .env  # Mac/Linux
# 또는
type nul > .env  # Windows
```

### 4.2 `.env` 파일 내용 작성

```env
GEMINI_API_KEY=여기에_발급받은_API_Key_입력
```

예시:
```env
GEMINI_API_KEY=AIzaSyDXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

### 4.3 `.gitignore` 설정

`.env` 파일이 Git에 업로드되지 않도록 `.gitignore`에 추가합니다.

```gitignore
# .gitignore 파일에 추가
.env
*.env
config.ini
```

### 4.4 Python 코드에서 사용하기

```python
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API Key 가져오기
api_key = os.getenv('GEMINI_API_KEY')
```

> **참고**: `python-dotenv` 패키지가 필요합니다.
> ```bash
> pip install python-dotenv
> ```

---

## 5. 설치 확인

모든 설정이 완료되었는지 확인합니다.

### 5.1 Python 버전 확인

```bash
conda activate ai
python --version
```

출력 예시: `Python 3.10.19`

### 5.2 패키지 설치 확인

```bash
pip list
```

다음 패키지들이 보여야 합니다:
- `google-generativeai`
- `Pillow`
- `pyperclip`

### 5.3 간단한 테스트 코드 실행

테스트 파일 생성: `test_setup.py`

```python
import google.generativeai as genai
from PIL import Image
import pyperclip

print("✅ google-generativeai 임포트 성공")
print("✅ Pillow (PIL) 임포트 성공")
print("✅ pyperclip 임포트 성공")
print("\n🎉 모든 패키지가 정상적으로 설치되었습니다!")

# Gemini API 연결 테스트 (API Key가 있다면)
import os
api_key = os.getenv('GEMINI_API_KEY')
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("\n✅ Gemini API 연결 성공!")
else:
    print("\n⚠️ GEMINI_API_KEY가 설정되지 않았습니다.")
    print("   .env 파일에 API Key를 추가하세요.")
```

실행:
```bash
conda activate ai
python test_setup.py
```

---

## 📌 자주 묻는 질문 (FAQ)

### Q1. conda 명령어가 인식되지 않아요

**A1**: 환경 변수에 conda 경로가 추가되어 있는지 확인하세요.

Windows:
```
D:\Utility\miniconda3\Scripts
D:\Utility\miniconda3\Library\bin
```

### Q2. API Key를 잃어버렸어요

**A2**: Google AI Studio에서 기존 Key를 삭제하고 새로운 Key를 생성하세요.

### Q3. 일일 요청 제한을 초과하면 어떻게 되나요?

**A3**: 다음 날 자정(UTC 기준)에 제한이 리셋됩니다. 유료 플랜으로 업그레이드할 수도 있습니다.

### Q4. 가상환경을 삭제하고 싶어요

**A4**:
```bash
conda deactivate
conda remove -n ai --all
```

---

## 🔗 유용한 링크

- [Miniconda 다운로드](https://docs.conda.io/en/latest/miniconda.html)
- [Google AI Studio](https://aistudio.google.com/)
- [Gemini API 문서](https://ai.google.dev/docs)
- [Python Pillow 문서](https://pillow.readthedocs.io/)

---

## ✅ 체크리스트

설정이 완료되었는지 확인하세요:

- [ ] 미니콘다 설치 확인
- [ ] `ai` 가상환경 생성
- [ ] 가상환경 활성화 가능
- [ ] Gemini API Key 발급
- [ ] `.env` 파일에 API Key 저장
- [ ] 필수 패키지 설치 (`google-generativeai`, `pillow`, `pyperclip`)
- [ ] 테스트 코드 실행 성공

---

**작성일**: 2026-01-14
**버전**: 1.0
**다음 단계**: [plan.md](plan.md) 참고하여 프로젝트 개발 시작
