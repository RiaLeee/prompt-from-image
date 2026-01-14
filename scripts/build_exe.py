"""
프롬프트 생성기 - 자동 빌드 스크립트
PyInstaller를 사용하여 exe 파일 생성 및 배포 폴더 구성
"""

import os
import subprocess
import shutil
from pathlib import Path
from datetime import datetime


def main():
    """메인 빌드 프로세스"""

    print("=" * 60)
    print("🚀 프롬프트 생성기 - 자동 빌드 시작")
    print("=" * 60)
    print()

    # 1. 기존 빌드 폴더 정리
    print("📁 기존 빌드 폴더 정리 중...")
    clean_build_folders()
    print("✅ 정리 완료\n")

    # 2. PyInstaller 설치 확인
    print("🔍 PyInstaller 확인 중...")
    check_pyinstaller()
    print("✅ PyInstaller 준비됨\n")

    # 3. 빌드 실행
    print("🔨 EXE 파일 빌드 시작...")
    build_exe()
    print("✅ 빌드 완료\n")

    # 4. 배포 폴더 구성
    print("📦 배포 폴더 구성 중...")
    prepare_release()
    print("✅ 배포 폴더 준비 완료\n")

    # 5. 완료 메시지
    print("=" * 60)
    print("🎉 빌드 완료!")
    print("=" * 60)
    print()
    print("📂 배포 파일 위치:")
    print(f"   {Path('release').absolute()}")
    print()
    print("🎯 다음 단계:")
    print("   1. release/prompt-maker-v1.0 폴더 테스트")
    print("   2. 프롬프트생성기.exe 실행 확인")
    print("   3. ZIP 파일로 압축")
    print()


def clean_build_folders():
    """기존 빌드 폴더 삭제"""
    folders = ['build', 'dist', '__pycache__']
    files = ['*.spec']

    for folder in folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"   삭제: {folder}/")

    # .spec 파일 삭제
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   삭제: {spec_file}")


def check_pyinstaller():
    """PyInstaller 설치 확인 및 설치"""
    try:
        import PyInstaller
        print(f"   PyInstaller 버전: {PyInstaller.__version__}")
    except ImportError:
        print("   PyInstaller가 설치되지 않았습니다.")
        print("   설치 중...")
        subprocess.check_call(['pip', 'install', 'pyinstaller'])
        print("   ✅ PyInstaller 설치 완료")


def build_exe():
    """PyInstaller로 EXE 파일 빌드"""

    # PyInstaller 명령어 구성
    cmd = [
        'pyinstaller',
        '--name', '프롬프트생성기',
        '--windowed',  # 콘솔 창 숨김
        '--onedir',    # 폴더 형태 (빠른 실행)
        '--clean',     # 깨끗한 빌드

        # 추가 파일
        '--add-data', '.env.example;.',

        # 숨겨진 import (자동 감지 안 되는 모듈)
        '--hidden-import', 'PIL._tkinter_finder',
        '--hidden-import', 'google.genai',
        '--hidden-import', 'google.ai',
        '--hidden-import', 'google.ai.generativelanguage',

        # Google AI 패키지 전체 포함
        '--collect-all', 'google.genai',
        '--collect-all', 'google.ai',

        # src 폴더를 경로에 추가
        '--paths', 'src',

        # 메인 파일 (src 폴더 내)
        'src/promptmaker_gui.py'
    ]

    print("   명령어:")
    print(f"   {' '.join(cmd)}")
    print()
    print("   빌드 진행 중... (5-10분 소요)")
    print()

    # 빌드 실행
    result = subprocess.run(cmd, capture_output=False, text=True)

    if result.returncode != 0:
        print("\n❌ 빌드 실패!")
        exit(1)

    print("\n   ✅ EXE 파일 생성 완료")


def prepare_release():
    """배포용 폴더 구성"""

    # 배포 폴더 경로
    release_dir = Path('release')
    version = 'v1.0'
    app_dir = release_dir / f'prompt-maker-{version}'

    # 기존 폴더 삭제
    if release_dir.exists():
        shutil.rmtree(release_dir)

    # 새 폴더 생성
    app_dir.mkdir(parents=True)

    # dist 폴더 내용 복사
    dist_dir = Path('dist') / '프롬프트생성기'
    if dist_dir.exists():
        shutil.copytree(dist_dir, app_dir, dirs_exist_ok=True)
        print(f"   복사: dist/프롬프트생성기/ → {app_dir}/")
    else:
        print("   ⚠️  경고: dist/프롬프트생성기 폴더를 찾을 수 없습니다")
        return

    # 사용법.txt 생성
    create_user_guide(app_dir)

    # .env.example 복사 확인
    env_example = app_dir / '.env.example'
    if not env_example.exists():
        shutil.copy('.env.example', env_example)
        print(f"   복사: .env.example → {app_dir}/")

    # 폴더 구조 출력
    print()
    print("   📂 배포 폴더 구조:")
    print(f"   {app_dir}/")
    print(f"   ├── 프롬프트생성기.exe")
    print(f"   ├── _internal/         (라이브러리)")
    print(f"   ├── .env.example       (API Key 설정)")
    print(f"   └── 사용법.txt")


def create_user_guide(app_dir: Path):
    """사용자 가이드 파일 생성"""

    guide_content = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   🎨 AI 프롬프트 생성기 v1.0 - 사용법
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 시작하기

1. API Key 설정 (최초 1회)

   ① .env.example 파일을 찾습니다
   ② 파일 이름을 .env로 변경합니다
   ③ 메모장으로 열어서 다음과 같이 수정:

      GEMINI_API_KEY=여기에_발급받은_API_Key_입력

   ④ 저장하고 닫습니다

2. 프로그램 실행

   프롬프트생성기.exe를 더블클릭!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📸 사용 방법
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1단계: 이미지 선택
   - "파일 선택..." 버튼 클릭
   - JPG, PNG, WEBP 파일 선택
   - 이미지 1은 필수, 이미지 2는 선택사항

2단계: 텍스트 입력
   - 원하는 스타일이나 장면 설명
   - 예: "두 양갈래 소녀들이 하이파이브하고 있는 지브리 스타일로"

3단계: 프롬프트 생성
   - "프롬프트 생성하기" 버튼 클릭
   - 1-10초 대기

4단계: 결과 사용
   - "복사" 버튼: 프롬프트 클립보드 복사
   - "JSON 저장" 버튼: 파일로 저장
   - Midjourney, DALL-E 등에 붙여넣기


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔑 API Key 발급 방법
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. https://aistudio.google.com/app/apikey 접속
2. Google 계정 로그인
3. "Create API Key" 클릭
4. API Key 복사
5. .env 파일에 붙여넣기

💰 완전 무료! (하루 1,500회 요청 제한)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❓ 문제 해결
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Q1. 프로그램이 실행되지 않아요
A1. 백신 프로그램이 차단하는지 확인하세요
    Windows Defender 예외 설정이 필요할 수 있습니다

Q2. "API 연결 실패" 오류가 나요
A2.
   - .env 파일이 있는지 확인
   - API Key가 올바른지 확인
   - 인터넷 연결 확인

Q3. 이미지가 너무 크다고 나와요
A3. 이미지를 10MB 이하로 줄여주세요

Q4. 프롬프트가 영어로만 나와요
A4. 정상입니다! AI 이미지 생성 도구는 영어 프롬프트를 사용합니다


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 파일 구조
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

프롬프트생성기.exe      - 실행 파일 (이것을 더블클릭)
_internal/              - 필수 라이브러리 (삭제 금지!)
.env.example            - API Key 설정 예시
사용법.txt              - 이 파일
output/                 - JSON 결과 저장 폴더 (자동 생성)


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 보안 주의사항
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚠️  .env 파일에 있는 API Key는 절대 타인에게 공유하지 마세요!
⚠️  프로그램을 배포할 때 .env 파일은 제외하세요!


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

개발: Claude Code Assistant
버전: 1.0
날짜: 2026-01-14

"""

    guide_path = app_dir / '사용법.txt'
    guide_path.write_text(guide_content, encoding='utf-8')
    print(f"   생성: {guide_path}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ 사용자에 의해 중단됨")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
