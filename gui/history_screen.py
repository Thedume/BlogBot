import customtkinter as ctk
from tkinter import messagebox

from core.history_store import load_history, delete_entry


class HistoryScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        self._current_kind = "song"

        top_row = ctk.CTkFrame(self, fg_color="transparent")
        top_row.pack(fill="x", padx=24, pady=(20, 8))

        ctk.CTkLabel(top_row, text="기록", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkButton(
            top_row, text="← 메인으로", width=100, fg_color="transparent", border_width=1,
            text_color=("gray20", "gray80"),
            command=lambda: controller.show_screen("MainScreen")
        ).pack(side="right")

        tab_row = ctk.CTkFrame(self, fg_color="transparent")
        tab_row.pack(fill="x", padx=24, pady=(0, 12))

        self.song_tab_btn = ctk.CTkButton(tab_row, text="노래 소개", width=110, command=lambda: self._switch_tab("song"))
        self.song_tab_btn.pack(side="left", padx=(0, 8))

        self.code_tab_btn = ctk.CTkButton(tab_row, text="코딩 테스트", width=110, command=lambda: self._switch_tab("code"))
        self.code_tab_btn.pack(side="left")

        self.list_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_container.pack(fill="both", expand=True, padx=24, pady=(0, 20))

        self.empty_label = ctk.CTkLabel(self.list_container, text="", text_color=("gray40", "gray60"))

    def on_show(self):
        """화면 전환 시 controller가 호출 — 항상 최신 목록으로 새로고침합니다."""
        self._switch_tab(self._current_kind)

    def _switch_tab(self, kind: str):
        self._current_kind = kind

        active_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"]
        inactive_color = "transparent"
        self.song_tab_btn.configure(fg_color=active_color if kind == "song" else inactive_color,
                                     border_width=0 if kind == "song" else 1)
        self.code_tab_btn.configure(fg_color=active_color if kind == "code" else inactive_color,
                                     border_width=0 if kind == "code" else 1)

        self._refresh_list()

    def _refresh_list(self):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        entries = load_history(self._current_kind)

        if not entries:
            ctk.CTkLabel(
                self.list_container, text="아직 작성한 기록이 없습니다.",
                text_color=("gray40", "gray60")
            ).pack(pady=20)
            return

        for entry in entries:
            self._build_row(entry)

    def _build_row(self, entry: dict):
        row = ctk.CTkFrame(self.list_container, fg_color=("gray95", "gray17"), corner_radius=8)
        row.pack(fill="x", pady=4)

        text_col = ctk.CTkFrame(row, fg_color="transparent")
        text_col.pack(side="left", fill="x", expand=True, padx=12, pady=10)

        ctk.CTkLabel(text_col, text=entry["title"], anchor="w", font=ctk.CTkFont(weight="bold")).pack(fill="x")
        date_display = entry["created_at"].replace("T", " ")
        ctk.CTkLabel(text_col, text=date_display, anchor="w", text_color=("gray40", "gray60"), font=ctk.CTkFont(size=12)).pack(fill="x")

        btn_col = ctk.CTkFrame(row, fg_color="transparent")
        btn_col.pack(side="right", padx=12)

        ctk.CTkButton(btn_col, text="미리보기", width=80, command=lambda e=entry: self._on_preview(e)).pack(side="left", padx=4)
        ctk.CTkButton(btn_col, text="삭제", width=60, fg_color="transparent", border_width=1,
                      text_color=("red", "#ff6b6b"),
                      command=lambda e=entry: self._on_delete(e)).pack(side="left", padx=4)

    def _on_preview(self, entry: dict):
        self.controller.show_result(
            kind=self._current_kind,
            blog_title=entry["title"],
            html=entry["html"],
            inputs=entry["inputs"],
            return_screen="HistoryScreen",
            save_to_history=False,
        )

    def _on_delete(self, entry: dict):
        confirmed = messagebox.askyesno("삭제 확인", f"'{entry['title']}' 기록을 정말 삭제하시겠습니까?")
        if not confirmed:
            return
        delete_entry(self._current_kind, entry["id"])
        self._refresh_list()