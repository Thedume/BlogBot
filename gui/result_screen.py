import customtkinter as ctk
from tkinter import filedialog, messagebox

from core.history_store import add_entry


class ResultScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self._current_kind = None
        self._current_title = None
        self._current_html = None
        self._return_screen = None

        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(top_row, text="결과", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        ctk.CTkButton(top_row, text="HTML 복사", width=110, command=self._on_copy_html).pack(side="right")
        ctk.CTkButton(top_row, text="파일 저장", width=110, command=self._on_save).pack(side="right", padx=(0, 8))

        title_row = ctk.CTkFrame(self, fg_color="transparent")
        title_row.pack(fill="x", padx=24, pady=(0, 8))

        ctk.CTkLabel(title_row, text="블로그 제목", anchor="w", text_color=("gray40", "gray60"), font=ctk.CTkFont(size=12)).pack(fill="x")

        title_inner = ctk.CTkFrame(title_row, fg_color="transparent")
        title_inner.pack(fill="x", pady=(2, 0))

        self.title_entry = ctk.CTkEntry(title_inner, font=ctk.CTkFont(weight="bold"))
        self.title_entry.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(title_inner, text="제목 복사", width=90, command=self._on_copy_title).pack(side="left", padx=(8, 0))

        ctk.CTkLabel(self, text="생성된 HTML", anchor="w", text_color=("gray40", "gray60"), font=ctk.CTkFont(size=12)).pack(fill="x", padx=24, pady=(8, 2))

        self.html_view = ctk.CTkTextbox(self, font=ctk.CTkFont(family="Consolas", size=12))
        self.html_view.pack(fill="both", expand=True, padx=24, pady=(0, 8))

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
        return_screen: 뒤로가기 시 돌아갈 화면 이름
        save_to_history: True면 기록에 새로 저장 (기록 화면 재조회 시엔 False)
        """
        self._current_kind = kind
        self._current_title = blog_title
        self._current_html = html
        self._return_screen = return_screen

        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, blog_title)

        self.html_view.configure(state="normal")
        self.html_view.delete("1.0", "end")
        self.html_view.insert("1.0", html)
        self.html_view.configure(state="disabled")

        if save_to_history:
            add_entry(kind, blog_title, inputs, html)

        self.controller.show_screen("ResultScreen")

    def _on_copy_title(self):
        title = self.title_entry.get()
        if not title:
            return
        self.clipboard_clear()
        self.clipboard_append(title)
        messagebox.showinfo("복사 완료", "블로그 제목이 클립보드에 복사되었습니다.")

    def _on_copy_html(self):
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