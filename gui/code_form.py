import customtkinter as ctk

from core.templates import format_code_post, build_code_title
from gui.widgets import ResizableTextbox


class CodeFormScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(scroll, text="코딩 테스트 풀이 작성", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 16))

        row = ctk.CTkFrame(scroll, fg_color="transparent")
        row.pack(fill="x")

        lang_col = ctk.CTkFrame(row, fg_color="transparent")
        lang_col.pack(side="left", padx=(0, 8))
        ctk.CTkLabel(lang_col, text="사용 언어", anchor="w").pack(fill="x", pady=(0, 4))
        self.language = ctk.CTkEntry(lang_col, placeholder_text="C++ / Python / Java", width=140)
        self.language.pack(fill="x")

        title_col = ctk.CTkFrame(row, fg_color="transparent")
        title_col.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(title_col, text="문제 번호 + 제목", anchor="w").pack(fill="x", pady=(0, 4))
        self.problem_title = ctk.CTkEntry(title_col, placeholder_text="예: 백준 1000번 - A+B")
        self.problem_title.pack(fill="x")

        ctk.CTkLabel(scroll, text="문제 설명 + 예제 입출력", anchor="w").pack(fill="x", pady=(12, 4))
        self.problem = ResizableTextbox(scroll, height=100)
        self.problem.pack(fill="x")

        ctk.CTkLabel(scroll, text="풀이 설명", anchor="w").pack(fill="x", pady=(12, 4))
        self.solution = ResizableTextbox(scroll, height=80)
        self.solution.pack(fill="x")

        ctk.CTkLabel(scroll, text="코드", anchor="w").pack(fill="x", pady=(12, 4))
        self.code = ResizableTextbox(scroll, height=140, font=ctk.CTkFont(family="Consolas", size=13))
        self.code.pack(fill="x")

        self.error_label = ctk.CTkLabel(scroll, text="", text_color="red")
        self.error_label.pack(fill="x", pady=(8, 0))

        button_row = ctk.CTkFrame(self, fg_color="transparent")
        button_row.pack(fill="x", padx=24, pady=(0, 20))

        ctk.CTkButton(button_row, text="초기화", fg_color="transparent", border_width=1,
                      text_color=("gray20", "gray80"), command=self._on_reset).pack(side="left")
        ctk.CTkButton(button_row, text="취소", fg_color="transparent", border_width=1,
                      text_color=("gray20", "gray80"),
                      command=lambda: controller.show_screen("MainScreen")).pack(side="left", padx=(8, 0))
        ctk.CTkButton(button_row, text="미리보기 생성", command=self._on_submit).pack(side="right")

    def _on_reset(self):
        self.language.delete(0, "end")
        self.problem_title.delete(0, "end")
        self.problem.clear()
        self.solution.clear()
        self.code.clear()
        self.error_label.configure(text="")

    def _on_submit(self):
        self.error_label.configure(text="")
        language = self.language.get().strip()
        problem_title = self.problem_title.get().strip()
        problem = self.problem.get().strip()
        solution = self.solution.get().strip()
        code = self.code.get().strip()

        if not language or not problem_title:
            self.error_label.configure(text="사용 언어와 문제 제목을 입력해주세요.")
            return
        if not problem or not solution or not code:
            self.error_label.configure(text="문제 설명, 풀이, 코드를 모두 입력해주세요.")
            return

        blog_title = build_code_title(language, problem_title)
        html = format_code_post(problem_title, problem, solution, code)

        inputs = {
            "language": language,
            "problem_title": problem_title,
            "problem": problem,
            "solution": solution,
            "code": code,
        }
        self.controller.show_result(
            kind="code",
            blog_title=blog_title,
            html=html,
            inputs=inputs,
            return_screen="CodeFormScreen",
        )