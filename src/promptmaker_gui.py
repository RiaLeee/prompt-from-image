"""
AI 프롬프트 생성기 - Tkinter GUI 애플리케이션
이미지와 텍스트를 입력받아 AI가 프롬프트를 생성
"""

import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from datetime import datetime
from pathlib import Path
import pyperclip
from dotenv import load_dotenv
from PIL import Image, ImageTk
import threading
import webbrowser
import time

from gemini_api import GeminiPromptGenerator, test_api_connection


class PromptMakerApp:
    """프롬프트 생성기 GUI 애플리케이션"""

    def __init__(self, root):
        self.root = root
        self.root.title("🎨 AI 프롬프트 생성기 v1.0")
        self.root.geometry("900x800")
        self.root.resizable(True, True)

        # 환경변수 로드
        load_dotenv()

        # 변수 초기화
        self.image_paths = []  # 선택된 이미지 파일 경로
        self.image_labels = []  # 이미지 미리보기 라벨
        self.api_key_var = tk.StringVar(value=os.getenv('GEMINI_API_KEY', ''))
        self.user_text_var = tk.StringVar()
        self.result_json = None
        self.generator = None

        # UI 구성
        self._create_widgets()

        # 출력 폴더 생성
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)

    def _create_widgets(self):
        """UI 위젯 생성"""

        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 그리드 가중치 설정
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        row = 0

        # === 타이틀 ===
        title_label = ttk.Label(
            main_frame,
            text="🎨 AI 프롬프트 생성기",
            font=("맑은 고딕", 16, "bold")
        )
        title_label.grid(row=row, column=0, pady=(0, 20))
        row += 1

        # === 이미지 선택 섹션 ===
        image_frame = ttk.LabelFrame(main_frame, text="📸 참고 이미지 선택 (최대 3개)", padding="10")
        image_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        image_frame.columnconfigure(0, weight=1)
        image_frame.columnconfigure(1, weight=1)
        image_frame.columnconfigure(2, weight=1)
        row += 1

        # 이미지 경로 초기화
        self.image_paths = [None, None, None]

        # 이미지 1
        self.image1_frame = ttk.Frame(image_frame)
        self.image1_frame.grid(row=0, column=0, padx=5, pady=5)

        self.image1_label = ttk.Label(self.image1_frame, text="이미지 1\n(필수)", justify=tk.CENTER)
        self.image1_label.pack()

        self.image1_preview = ttk.Label(self.image1_frame, text="", relief=tk.SOLID, borderwidth=1)
        self.image1_preview.pack(pady=5)

        btn1 = ttk.Button(self.image1_frame, text="파일 선택...", command=lambda: self._select_image(0))
        btn1.pack()

        # 이미지 2
        self.image2_frame = ttk.Frame(image_frame)
        self.image2_frame.grid(row=0, column=1, padx=5, pady=5)

        self.image2_label = ttk.Label(self.image2_frame, text="이미지 2\n(선택사항)", justify=tk.CENTER)
        self.image2_label.pack()

        self.image2_preview = ttk.Label(self.image2_frame, text="", relief=tk.SOLID, borderwidth=1)
        self.image2_preview.pack(pady=5)

        btn2 = ttk.Button(self.image2_frame, text="파일 선택...", command=lambda: self._select_image(1))
        btn2.pack()

        # 이미지 3
        self.image3_frame = ttk.Frame(image_frame)
        self.image3_frame.grid(row=0, column=2, padx=5, pady=5)

        self.image3_label = ttk.Label(self.image3_frame, text="이미지 3\n(선택사항)", justify=tk.CENTER)
        self.image3_label.pack()

        self.image3_preview = ttk.Label(self.image3_frame, text="", relief=tk.SOLID, borderwidth=1)
        self.image3_preview.pack(pady=5)

        btn3 = ttk.Button(self.image3_frame, text="파일 선택...", command=lambda: self._select_image(2))
        btn3.pack()

        self.image_labels = [self.image1_label, self.image2_label, self.image3_label]

        # === 텍스트 입력 섹션 ===
        text_frame = ttk.LabelFrame(main_frame, text="✍️ 원하는 스타일/장면 입력", padding="10")
        text_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        text_frame.columnconfigure(0, weight=1)
        row += 1

        # 안내 텍스트
        help_label = ttk.Label(
            text_frame,
            text="예시: 두 양갈래 소녀들이 하이파이브하는 지브리 스타일, 사이버펑크 도시 배경의 고양이 전사 등",
            font=("맑은 고딕", 8),
            foreground="gray"
        )
        help_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.text_input = scrolledtext.ScrolledText(text_frame, height=4, wrap=tk.WORD, font=("맑은 고딕", 10))
        self.text_input.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # 플레이스홀더 텍스트
        self.placeholder_text = "원하는 이미지 스타일과 장면을 자유롭게 설명해주세요..."
        self.text_input.insert("1.0", self.placeholder_text)
        self.text_input.config(foreground="gray")
        self.is_placeholder = True

        # 포커스 이벤트 바인딩
        self.text_input.bind("<FocusIn>", self._on_text_focus_in)
        self.text_input.bind("<FocusOut>", self._on_text_focus_out)

        # === API Key 입력 ===
        api_frame = ttk.LabelFrame(main_frame, text="🔑 Gemini API Key", padding="10")
        api_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        api_frame.columnconfigure(0, weight=1)
        row += 1

        self.api_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, show="*", font=("맑은 고딕", 9))
        self.api_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))

        ttk.Button(api_frame, text="API 연결 테스트", command=self._test_api).grid(row=0, column=1, padx=(0, 10))

        # 사용량 확인 링크 버튼
        usage_btn = ttk.Button(api_frame, text="📊 사용량 확인", command=self._open_usage_page)
        usage_btn.grid(row=0, column=2)

        # === 생성 버튼 ===
        self.generate_btn = ttk.Button(
            main_frame,
            text="🚀 프롬프트 생성하기",
            command=self._generate_prompt,
            style="Accent.TButton"
        )
        self.generate_btn.grid(row=row, column=0, pady=10)
        row += 1

        # === 프로그레스바 ===
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress_frame.columnconfigure(0, weight=1)

        self.progress_label = ttk.Label(self.progress_frame, text="", font=("맑은 고딕", 9))
        self.progress_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='indeterminate',
            length=400
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # 초기에는 숨김
        self.progress_frame.grid_remove()
        row += 1

        # === 결과 표시 섹션 ===
        result_frame = ttk.LabelFrame(main_frame, text="📋 생성된 프롬프트", padding="10")
        result_frame.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(row, weight=1)
        row += 1

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            height=15,
            wrap=tk.WORD,
            font=("Consolas", 9),
            state=tk.DISABLED
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 버튼 프레임
        btn_frame = ttk.Frame(result_frame)
        btn_frame.grid(row=1, column=0, pady=(5, 0))

        ttk.Button(btn_frame, text="📋 복사", command=self._copy_result).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="💾 JSON 저장", command=self._save_result).pack(side=tk.LEFT, padx=5)

        # === 상태바 ===
        self.status_var = tk.StringVar(value="준비 완료")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=row, column=0, sticky=(tk.W, tk.E))

    def _select_image(self, index: int):
        """이미지 파일 선택"""
        file_path = filedialog.askopenfilename(
            title=f"이미지 {index + 1} 선택",
            filetypes=[
                ("이미지 파일", "*.jpg *.jpeg *.png *.webp"),
                ("모든 파일", "*.*")
            ]
        )

        if file_path:
            try:
                # 이미지 로드 및 검증
                img = Image.open(file_path)

                # 파일 크기 체크
                file_size = os.path.getsize(file_path)
                if file_size > 10 * 1024 * 1024:  # 10MB
                    messagebox.showerror("오류", "이미지 파일이 10MB를 초과합니다.")
                    return

                # 리스트 크기 조정
                while len(self.image_paths) <= index:
                    self.image_paths.append(None)

                # 경로 저장
                self.image_paths[index] = file_path

                # 미리보기 표시
                self._show_image_preview(img, index)

                # 라벨 업데이트
                filename = Path(file_path).name
                self.image_labels[index].config(text=f"이미지 {index + 1}\n{filename}")

                self.status_var.set(f"이미지 {index + 1} 선택됨: {filename}")

            except Exception as e:
                messagebox.showerror("오류", f"이미지 로드 실패:\n{str(e)}")

    def _show_image_preview(self, img: Image.Image, index: int):
        """이미지 미리보기 표시"""
        # 썸네일 생성 (150x150)
        img_copy = img.copy()
        img_copy.thumbnail((150, 150))

        # Tkinter 이미지로 변환
        photo = ImageTk.PhotoImage(img_copy)

        # 미리보기 업데이트
        if index == 0:
            self.image1_preview.config(image=photo)
            self.image1_preview.image = photo  # 참조 유지
        elif index == 1:
            self.image2_preview.config(image=photo)
            self.image2_preview.image = photo
        elif index == 2:
            self.image3_preview.config(image=photo)
            self.image3_preview.image = photo

    def _on_text_focus_in(self, event):
        """텍스트 입력창 포커스 시 플레이스홀더 제거"""
        if self.is_placeholder:
            self.text_input.delete("1.0", tk.END)
            self.text_input.config(foreground="black")
            self.is_placeholder = False

    def _on_text_focus_out(self, event):
        """텍스트 입력창 포커스 해제 시 빈 경우 플레이스홀더 복원"""
        if not self.text_input.get("1.0", tk.END).strip():
            self.text_input.insert("1.0", self.placeholder_text)
            self.text_input.config(foreground="gray")
            self.is_placeholder = True

    def _open_usage_page(self):
        """API 사용량 확인 페이지 열기"""
        url = "https://aistudio.google.com/usage"

        # 크롬 브라우저로 열기 시도
        try:
            # Windows에서 크롬 경로들
            chrome_paths = [
                "C:/Program Files/Google/Chrome/Application/chrome.exe",
                "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
                os.path.expanduser("~") + "/AppData/Local/Google/Chrome/Application/chrome.exe"
            ]

            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break

            if chrome_path:
                webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
                webbrowser.get('chrome').open(url)
                self.status_var.set("크롬에서 사용량 대시보드를 열었습니다")
            else:
                # 크롬이 없으면 기본 브라우저 사용
                webbrowser.open(url)
                self.status_var.set("브라우저에서 사용량 대시보드를 열었습니다")
        except Exception:
            # 오류 발생 시 기본 브라우저 사용
            webbrowser.open(url)
            self.status_var.set("브라우저에서 사용량 대시보드를 열었습니다")

    def _test_api(self):
        """API 연결 테스트"""
        api_key = self.api_key_var.get().strip()

        if not api_key:
            messagebox.showwarning("경고", "API Key를 입력하세요.")
            return

        self.status_var.set("API 연결 테스트 중...")
        self.root.update()

        def test_thread():
            try:
                if test_api_connection(api_key):
                    self.root.after(0, lambda: messagebox.showinfo(
                        "성공",
                        "✅ API 연결 성공!\n\n모델: gemini-2.5-flash\n상태: 정상 작동\n\n📊 사용량 확인: Google AI Studio에서 확인 가능"
                    ))
                    self.root.after(0, lambda: self.status_var.set("API 연결 성공"))
                else:
                    self.root.after(0, lambda: messagebox.showerror("실패", "❌ API 연결 실패\n\nAPI Key를 확인하거나\n사용량 제한을 확인하세요."))
                    self.root.after(0, lambda: self.status_var.set("API 연결 실패"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("오류", f"테스트 실패:\n{str(e)}"))
                self.root.after(0, lambda: self.status_var.set("준비 완료"))

        threading.Thread(target=test_thread, daemon=True).start()

    def _generate_prompt(self):
        """프롬프트 생성"""
        # 입력 검증
        api_key = self.api_key_var.get().strip()
        user_text = self.text_input.get("1.0", tk.END).strip()

        # 플레이스홀더 텍스트 제외
        if self.is_placeholder or user_text == self.placeholder_text:
            user_text = ""

        if not api_key:
            messagebox.showwarning("경고", "API Key를 입력하세요.")
            return

        # 이미지 검증 (None이 아닌 것만 필터링)
        valid_images = [img for img in self.image_paths if img is not None]

        if not valid_images:
            messagebox.showwarning("경고", "최소 1개의 이미지를 선택하세요.")
            return

        if not user_text:
            messagebox.showwarning("경고", "텍스트 명령어를 입력하세요.")
            return

        # UI 업데이트: 버튼 비활성화, 프로그레스바 표시
        self.generate_btn.config(state=tk.DISABLED)
        self.progress_frame.grid()
        self.progress_label.config(text="🔄 프롬프트 생성 준비 중... (예상 소요 시간: 10-30초)")
        self.progress_bar.start(10)  # 10ms마다 애니메이션
        self.status_var.set("프롬프트 생성 중...")
        self.root.update()

        # 타이머를 위한 플래그
        self.generating = True
        start_time = time.time()

        # 타이머 업데이트 함수
        def update_timer():
            if self.generating:
                elapsed = int(time.time() - start_time)
                self.progress_label.config(text=f"🎨 AI가 프롬프트 생성 중... (경과 시간: {elapsed}초 / 평균 15-20초 소요)")
                self.root.after(1000, update_timer)  # 1초마다 업데이트

        def generate_thread():
            try:
                # Generator 초기화
                self.root.after(0, lambda: self.progress_label.config(text="⚙️ Gemini API 초기화 중... (1-2초)"))
                if not self.generator:
                    self.generator = GeminiPromptGenerator(api_key)

                time.sleep(0.5)  # 초기화 시간

                # 타이머 시작
                self.root.after(0, update_timer)

                # 프롬프트 생성
                result = self.generator.generate_prompt(valid_images, user_text)

                # 타이머 중지
                self.generating = False
                elapsed = int(time.time() - start_time)

                # 결과 표시
                self.root.after(0, lambda: self._display_result(result))
                self.root.after(0, lambda: self.status_var.set(f"✅ 프롬프트 생성 완료! (소요 시간: {elapsed}초)"))
                self.root.after(0, lambda: self.progress_label.config(text=f"✅ 프롬프트 생성 완료! (총 {elapsed}초 소요)"))

            except Exception as e:
                self.generating = False
                self.root.after(0, lambda: messagebox.showerror("오류", f"프롬프트 생성 실패:\n{str(e)}"))
                self.root.after(0, lambda: self.status_var.set("준비 완료"))
                self.root.after(0, lambda: self.progress_label.config(text="❌ 생성 실패"))

            finally:
                # UI 복원
                self.root.after(0, lambda: self.progress_bar.stop())
                self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL))
                # 3초 후 프로그레스바 숨김
                self.root.after(3000, lambda: self.progress_frame.grid_remove())

        threading.Thread(target=generate_thread, daemon=True).start()

    def _display_result(self, result: dict):
        """결과 표시"""
        self.result_json = result

        # JSON을 보기 좋게 포맷
        json_str = json.dumps(result, indent=2, ensure_ascii=False)

        # 텍스트 박스에 표시
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", json_str)
        self.result_text.config(state=tk.DISABLED)

    def _copy_result(self):
        """결과 클립보드 복사"""
        if not self.result_json:
            messagebox.showwarning("경고", "생성된 프롬프트가 없습니다.")
            return

        try:
            # final_prompt만 복사
            final_prompt = self.result_json.get('prompts', {}).get('final_prompt', '')

            if final_prompt:
                pyperclip.copy(final_prompt)
                messagebox.showinfo("성공", "📋 final_prompt가 클립보드에 복사되었습니다!")
                self.status_var.set("클립보드에 복사됨")
            else:
                messagebox.showwarning("경고", "final_prompt를 찾을 수 없습니다.")

        except Exception as e:
            messagebox.showerror("오류", f"복사 실패:\n{str(e)}")

    def _save_result(self):
        """결과 JSON 파일 저장"""
        if not self.result_json:
            messagebox.showwarning("경고", "생성된 프롬프트가 없습니다.")
            return

        try:
            # 기본 파일명 생성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"prompt_{timestamp}.json"

            # 파일 저장 대화상자
            file_path = filedialog.asksaveasfilename(
                title="JSON 파일 저장",
                initialdir=self.output_dir,
                initialfile=default_filename,
                defaultextension=".json",
                filetypes=[("JSON 파일", "*.json"), ("모든 파일", "*.*")]
            )

            if file_path:
                # JSON 저장
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(self.result_json, f, indent=2, ensure_ascii=False)

                messagebox.showinfo("성공", f"💾 파일이 저장되었습니다:\n{file_path}")
                self.status_var.set(f"파일 저장됨: {Path(file_path).name}")

        except Exception as e:
            messagebox.showerror("오류", f"저장 실패:\n{str(e)}")


def main():
    """메인 함수"""
    root = tk.Tk()

    # 스타일 설정
    style = ttk.Style()
    style.theme_use('clam')

    # 앱 실행
    app = PromptMakerApp(root)

    # 메인 루프
    root.mainloop()


if __name__ == "__main__":
    main()
