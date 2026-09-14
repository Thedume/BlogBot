import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterweb import HtmlFrame

from core.history_store import add_entry


class ResultScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        # 현재 표시 중인 데이터 (뒤로가기/저장/복사 시 사용)
        self._current_kind = None
        self._current_title = None
        self._current_html = None
        self._return_screen = None

        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(top_row, text="미리보기", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        ctk.CTkButton(top_row, text="복사하기", width=110, command=self._on_copy).pack(side="right", padx=(8, 0))
        ctk.CTkButton(top_row, text="파일 저장", width=110, command=self._on_save).pack(side="right")

        self.html_frame = HtmlFrame(self, messages_enabled=False)
        self.html_frame.pack(fill="both", expand=True, padx=24, pady=(0, 8))

        ctk.CTkButton(
            self, text="← 수정하러 돌아가기", fg_color="transparent", border_width=1,
            text_color=("gray20", "gray80"), command=self._on_back
        ).pack(padx=24, pady=(0, 20), anchor="w")

    def show_result(self, kind: str, blog_title: str, html: str, inputs: dict, return_screen: str, save_to_history: bool = True):
        """
        kind: 'song' 또는 'code'
        blog_title: 블로그 제목
        html: 생성된 HTML
        inputs: 폼 입력값 전체 (기록 저장용)
        return_screen: 뒤로가기 시 돌아갈 화면 이름 ('SongFormScreen' / 'CodeFormScreen')
        save_to_history: True면 기록에 새로 저장 (기록 화면에서 재조회할 땐 False로 호출)
        """
        self._current_kind = kind
        self._current_title = blog_title
        self._current_html = html
        self._return_screen = return_screen

        self.html_frame.load_html(html)

        if save_to_history:
            add_entry(kind, blog_title, inputs, html)

        self.controller.show_screen("ResultScreen")

    def _on_copy(self):
        if not self._current_html:
            return
        self.clipboard_clear()
        self.clipboard_append(self._current_html)
        messagebox.showinfo("복사 완료", "HTML이 클립보드에 복사되었습니다.")

    def _on_save(self):
        if not self._current_html:
            return
        default_name = "song_post.html" if self._current_kind == "song" else "code_post.html"
        path = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile=default_name,
            filetypes=[("HTML 파일", "*.html")]
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            f.write(self._current_html)
        messagebox.showinfo("저장 완료", f"파일이 저장되었습니다.\n{path}")

    def _on_back(self):
        self.controller.show_screen(self._return_screen or "MainScreen")