# 🚀 EXE 파일 빌드 가이드

이 문서는 **프롬프트 생성기**를 독립 실행형 `.exe` 파일로 만드는 방법을 설명합니다.

---

## 📋 목차

- [사전 준비](#사전-준비)
- [빌드 방법](#빌드-방법)
- [배포 방법](#배포-방법)
- [문제 해결](#문제-해결)

---

## 🛠️ 사전 준비

### 1. PyInstaller 설치

```bash
# 가상환경 활성화
conda activate ai

# PyInstaller 설치
pip install pyinstaller
```

### 2. 프로젝트 확인

다음 파일들이 있는지 확인:
- `promptmaker_gui.py` (메인 파일)
- `gemini_api.py` (API 모듈)
- `requirements.txt` (의존성)
- `.env.example` (API Key 예시)

---

## 🔨 빌드 방법

### 방법 1: 자동 빌드 스크립트 사용 (추천)

```bash
# Windows
python build_exe.py

# 또는 직접 실행
build_exe.py
```

**결과:**
- `dist/프롬프트생성기/` 폴더 생성
- 내부에 실행 파일과 필수 라이브러리 포함

---

### 방법 2: 수동 빌드

#### 옵션 A: 폴더 형태 (추천 - 빠르고 안정적)

```bash
pyinstaller --name "프롬프트생성기" ^
            --windowed ^
            --onedir ^
            --icon=NONE ^
            --add-data ".env.example;." ^
            --hidden-import "PIL._tkinter_finder" ^
            --collect-all google.genai ^
            --collect-all google.ai ^
            promptmaker_gui.py
```

**특징:**
- 빠른 실행 속도
- 폴더 + 실행 파일 형태
- 용량: 약 150MB

---

#### 옵션 B: 단일 파일 (간단하지만 느림)

```bash
pyinstaller --name "프롬프트생성기" ^
            --windowed ^
            --onefile ^
            --icon=NONE ^
            --add-data ".env.example;." ^
            --hidden-import "PIL._tkinter_finder" ^
            --collect-all google.genai ^
            --collect-all google.ai ^
            promptmaker_gui.py
```

**특징:**
- 단일 `.exe` 파일
- 실행 시 임시 압축 해제 (느림)
- 용량: 약 80MB

---

## 📦 배포 방법

### 1. 빌드 완료 후 구조 확인

```
dist/
└── 프롬프트생성기/
    ├── 프롬프트생성기.exe      ⬅️ 실행 파일
    ├── _internal/              (의존성 라이브러리)
    └── .env.example            (API Key 설정 예시)
```

---

### 2. 배포 폴더 만들기

#### 자동 생성 (build_exe.py 사용 시)

```
release/
└── prompt-maker-v1.0/
    ├── 프롬프트생성기.exe
    ├── _internal/
    ├── .env.example
    └── 사용법.txt
```

#### 수동 생성

```bash
# 1. 배포 폴더 생성
mkdir release
mkdir release\prompt-maker-v1.0

# 2. 빌드 파일 복사
xcopy /E /I dist\프롬프트생성기 release\prompt-maker-v1.0

# 3. 사용 설명서 복사
copy 사용법.txt release\prompt-maker-v1.0\
```

---

### 3. ZIP 파일 생성

#### Windows (탐색기)
1. `release\prompt-maker-v1.0` 폴더 우클릭
2. **"보내기 > 압축(ZIP) 폴더"** 선택
3. `prompt-maker-v1.0.zip` 생성 완료

#### Windows (명령어)
```bash
# PowerShell
Compress-Archive -Path "release\prompt-maker-v1.0" -DestinationPath "release\prompt-maker-v1.0.zip"
```

---

## 🎯 최종 사용자 사용 방법

### 배포된 ZIP 파일 사용

1. **다운로드**
   - `prompt-maker-v1.0.zip` 다운로드

2. **압축 해제**
   - 원하는 위치에 ZIP 파일 압축 해제
   - 예: `C:\프로그램\prompt-maker-v1.0\`

3. **실행**
   - `프롬프트생성기.exe` 더블클릭
   - Python 설치 불필요!

4. **API Key 설정** (최초 1회)
   - `.env.example` 파일을 `.env`로 이름 변경
   - 메모장으로 열어서 API Key 입력
   ```
   GEMINI_API_KEY=여기에_발급받은_API_Key_입력
   ```

---

## 🔍 빌드 옵션 설명

| 옵션 | 설명 |
|------|------|
| `--name` | 실행 파일 이름 |
| `--windowed` | 콘솔 창 숨김 (GUI 전용) |
| `--onedir` | 폴더 형태로 빌드 (빠름) |
| `--onefile` | 단일 exe 파일 (느림) |
| `--icon` | 아이콘 파일 (.ico) |
| `--add-data` | 추가 파일 포함 |
| `--hidden-import` | 자동 감지 안 되는 모듈 |
| `--collect-all` | 패키지 전체 포함 |

---

## ⚠️ 문제 해결

### Q1. "프롬프트생성기.exe가 실행되지 않아요"

**확인 사항:**
1. 백신 프로그램이 차단하는지 확인
2. Windows Defender 예외 설정
3. `_internal` 폴더가 같은 위치에 있는지 확인

**해결:**
```bash
# 빌드 다시 시도
rmdir /S dist
rmdir /S build
python build_exe.py
```

---

### Q2. "Import Error: No module named ..."

**원인:** 필수 모듈이 누락됨

**해결:**
```bash
# .spec 파일 수정 또는 빌드 시 추가
pyinstaller --hidden-import 모듈이름 ...
```

---

### Q3. "API 연결 실패"

**원인:** `.env` 파일 누락

**해결:**
1. `.env.example`을 `.env`로 복사
2. API Key 입력 확인
3. 프로그램 재시작

---

### Q4. "실행 파일이 너무 커요 (200MB+)"

**정상입니다:**
- Python 인터프리터 포함
- 모든 의존성 라이브러리 포함
- Tkinter GUI 라이브러리 포함
- Google AI 라이브러리 포함

**용량 줄이기:**
```bash
# UPX 압축 사용 (선택사항)
pip install pyinstaller[upx]
pyinstaller --upx-dir=upx경로 ...
```

---

### Q5. "빌드 시간이 너무 오래 걸려요"

**정상 소요 시간:**
- 첫 빌드: 5-10분
- 재빌드: 2-3분

**빠르게 하기:**
- `--onedir` 사용 (onefile보다 빠름)
- SSD 사용
- 백신 실시간 검사 일시 중지

---

## 📊 빌드 결과 비교

| 방식 | 파일 수 | 용량 | 실행 속도 | 배포 |
|------|---------|------|-----------|------|
| **폴더 형태** | 100+ | 150MB | 빠름 ⚡ | 폴더 전체 |
| **단일 파일** | 1 | 80MB | 느림 🐌 | exe 1개 |

**추천:** 폴더 형태 (안정적이고 빠름)

---

## 🎉 배포 체크리스트

빌드 전:
- [ ] 모든 기능 테스트 완료
- [ ] `.env.example` 파일 준비
- [ ] 버전 번호 확인 (v1.0)
- [ ] PyInstaller 최신 버전 설치

빌드 후:
- [ ] 실행 파일 동작 확인
- [ ] API 연결 테스트
- [ ] 이미지 업로드 테스트
- [ ] 프롬프트 생성 테스트
- [ ] 클립보드 복사 테스트

배포:
- [ ] `사용법.txt` 포함
- [ ] `.env.example` 포함
- [ ] ZIP 파일 이름 확인
- [ ] README 작성

---

## 📞 참고 자료

- [PyInstaller 공식 문서](https://pyinstaller.org/)
- [PyInstaller GitHub](https://github.com/pyinstaller/pyinstaller)
- [문제 해결 가이드](https://pyinstaller.readthedocs.io/en/stable/when-things-go-wrong.html)

---

**작성일**: 2026-01-14
**버전**: 1.0
