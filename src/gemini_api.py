"""
Gemini API 연동 모듈
이미지와 텍스트를 Gemini AI에 전송하여 프롬프트 생성
"""

import os
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
import google.genai as genai
from google.genai.types import GenerateContentConfig, Part
from PIL import Image
import io


class GeminiPromptGenerator:
    """Gemini API를 사용한 프롬프트 생성기"""

    def __init__(self, api_key: Optional[str] = None):
        """
        초기화

        Args:
            api_key: Gemini API Key (없으면 환경변수에서 로드)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')

        if not self.api_key:
            raise ValueError(
                "API Key가 설정되지 않았습니다. "
                ".env 파일에 GEMINI_API_KEY를 추가하거나 "
                "api_key 파라미터로 전달하세요."
            )

        # Gemini 클라이언트 초기화
        self.client = genai.Client(api_key=self.api_key)

    def _load_image(self, image_path: str) -> Image.Image:
        """
        이미지 파일 로드 및 검증

        Args:
            image_path: 이미지 파일 경로

        Returns:
            PIL Image 객체
        """
        try:
            img = Image.open(image_path)

            # 파일 크기 체크 (10MB 제한)
            file_size = os.path.getsize(image_path)
            max_size = 10 * 1024 * 1024  # 10MB

            if file_size > max_size:
                raise ValueError(f"이미지 파일이 너무 큽니다. (최대 10MB, 현재: {file_size / 1024 / 1024:.2f}MB)")

            # 지원 형식 체크
            if img.format not in ['JPEG', 'PNG', 'WEBP']:
                raise ValueError(f"지원하지 않는 이미지 형식입니다: {img.format}")

            return img

        except Exception as e:
            raise Exception(f"이미지 로드 실패: {str(e)}")

    def _create_system_prompt(self) -> str:
        """시스템 프롬프트 생성"""
        return """당신은 전문적인 AI 이미지 생성 프롬프트 엔지니어입니다.

사용자가 제공한 참고 이미지와 텍스트 명령어를 분석하여,
Midjourney, DALL-E, Stable Diffusion 등의 AI 이미지 생성 도구에서
최고 품질의 결과를 얻을 수 있는 전문적인 프롬프트를 생성하세요.

# 분석 항목:
1. 이미지 분석:
   - 색감 (color palette)
   - 조명 (lighting)
   - 구도 (composition)
   - 스타일 (art style)
   - 주요 객체 (main subjects)
   - 분위기 (mood/atmosphere)

2. 텍스트 명령어 파싱:
   - 원하는 장면/상황
   - 스타일 키워드
   - 특정 요구사항

# 출력 형식:
반드시 아래 JSON 구조로 출력하세요 (JSON만 출력하고 다른 텍스트는 포함하지 마세요):
{
  "meta": {
    "version": "3.0",
    "engine": "gemini-2.5-flash",
    "generated_at": "[ISO 8601 timestamp]"
  },
  "inputs": {
    "reference_images_count": [이미지 개수],
    "user_scene_text": "[사용자가 입력한 텍스트]"
  },
  "prompts": {
    "style_prompt": "[스타일 중심의 상세한 프롬프트 - 200단어 이상, 영어로 작성]",
    "scene_prompt": "[장면 중심의 상세한 프롬프트 - 영어로 작성]",
    "final_prompt": "[최종 통합 프롬프트 - 바로 사용 가능, 영어로 작성]"
  }
}

# 프롬프트 작성 규칙:
- 모든 프롬프트는 영어로 작성
- 전문적인 사진/렌더링 용어 사용 (volumetric lighting, subsurface scattering 등)
- 구체적이고 상세한 묘사
- 예술 스타일 명확히 지정 (Studio Ghibli, Pixar, Unreal Engine 5 등)
- 기술적 품질 키워드 포함 (8K, masterpiece, high-fidelity 등)
- JSON 외에 다른 텍스트는 절대 출력하지 마세요
"""

    def generate_prompt(
        self,
        image_paths: List[str],
        user_text: str
    ) -> Dict[str, Any]:
        """
        프롬프트 생성

        Args:
            image_paths: 참고 이미지 파일 경로 리스트 (1~2개)
            user_text: 사용자가 입력한 스타일/장면 설명

        Returns:
            생성된 프롬프트 JSON 딕셔너리
        """
        # 입력 검증
        if not image_paths:
            raise ValueError("최소 1개의 이미지가 필요합니다.")

        if len(image_paths) > 3:
            raise ValueError("최대 3개의 이미지만 지원합니다.")

        if not user_text or not user_text.strip():
            raise ValueError("텍스트 명령어를 입력하세요.")

        try:
            # 이미지 로드 및 파일 객체로 변환
            image_parts = []
            for img_path in image_paths:
                img = self._load_image(img_path)
                # 이미지를 바이트로 변환
                img_byte_arr = io.BytesIO()
                img.save(img_byte_arr, format=img.format or 'PNG')
                img_byte_arr.seek(0)

                # Part 객체 생성
                image_parts.append(Part.from_bytes(
                    data=img_byte_arr.read(),
                    mime_type=f"image/{(img.format or 'PNG').lower()}"
                ))

            # 프롬프트 구성
            system_prompt = self._create_system_prompt()

            # 사용자 메시지
            user_message = f"""
참고 이미지를 분석하고, 다음 텍스트 명령어에 맞는 프롬프트를 생성하세요:

사용자 요청: {user_text}

위의 JSON 형식으로만 응답하세요. 다른 텍스트는 포함하지 마세요.
"""

            # 콘텐츠 구성
            contents = [
                Part.from_text(text=system_prompt),
                Part.from_text(text=user_message),
            ] + image_parts

            # Gemini API 호출
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=contents,
                config=GenerateContentConfig(
                    temperature=0.7,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )

            # 응답 파싱
            response_text = response.text.strip()

            # JSON 추출 (마크다운 코드 블록 제거)
            if response_text.startswith('```'):
                # ```json ... ``` 형태 처리
                lines = response_text.split('\n')
                response_text = '\n'.join(lines[1:-1])

            # JSON 파싱
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # JSON 파싱 실패 시, { } 사이의 내용만 추출 시도
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end > start:
                    result = json.loads(response_text[start:end])
                else:
                    raise

            # 타임스탬프 추가 (없는 경우)
            if 'meta' in result and 'generated_at' not in result['meta']:
                result['meta']['generated_at'] = datetime.utcnow().isoformat() + 'Z'

            return result

        except Exception as e:
            raise Exception(f"프롬프트 생성 실패: {str(e)}")

    def save_to_file(self, prompt_data: Dict[str, Any], output_path: str):
        """
        생성된 프롬프트를 JSON 파일로 저장

        Args:
            prompt_data: 프롬프트 데이터
            output_path: 저장할 파일 경로
        """
        try:
            # 디렉토리 생성
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # JSON 저장
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(prompt_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            raise Exception(f"파일 저장 실패: {str(e)}")


# 간단한 테스트 함수
def test_api_connection(api_key: str) -> bool:
    """
    API 연결 테스트

    Args:
        api_key: Gemini API Key

    Returns:
        연결 성공 여부
    """
    try:
        client = genai.Client(api_key=api_key)

        # 간단한 테스트 요청
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=Part.from_text(text='Hello')
        )

        return bool(response.text)
    except Exception as e:
        print(f"API 연결 실패: {str(e)}")
        return False


if __name__ == "__main__":
    # 테스트 코드
    from dotenv import load_dotenv

    load_dotenv()

    api_key = os.getenv('GEMINI_API_KEY')

    if api_key:
        print("API 연결 테스트 중...")
        if test_api_connection(api_key):
            print("✅ API 연결 성공!")
        else:
            print("❌ API 연결 실패")
    else:
        print("❌ .env 파일에 GEMINI_API_KEY를 설정하세요.")
