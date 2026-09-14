import customtkinter as ctk
from tkinter import messagebox

from core.config_store import load_config, save_config


class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.pack(fill="both", expand=True, padx=24, pady=24)

        top_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        top_row.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(top_row, text="설정", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        ctk.CTkButton(
            top_row, text="← 메인으로", width=100, fg_color="transparent", border_width=1,
            text_color=("gray20", "gray80"),
            command=lambda: controller.show_screen("MainScreen")
        ).pack(side="right")

        form = ctk.CTkFrame(wrapper, fg_color="transparent")
        form.pack(fill="x")

        ctk.CTkLabel(form, text="Spotify Client ID", anchor="w").pack(fill="x", pady=(0, 4))
        self.client_id = ctk.CTkEntry(form)
        self.client_id.pack(fill="x")

        ctk.CTkLabel(form, text="Spotify Client Secret", anchor="w").pack(fill="x", pady=(12, 4))
        self.client_secret = ctk.CTkEntry(form, show="•")
        self.client_secret.pack(fill="x")

        ctk.CTkLabel(
            form,
            text="Spotify 링크를 입력하지 않고 사용할 경우, 이 설정은 건너뛰어도 됩니다.",
            anchor="w", text_color=("gray40", "gray60"), font=ctk.CTkFont(size=12),
            wraplength=500, justify="left"
        ).pack(fill="x", pady=(8, 0))

        self.status_label = ctk.CTkLabel(form, text="", anchor="w")
        self.status_label.pack(fill="x", pady=(12, 0))

        ctk.CTkButton(wrapper, text="저장", width=100, command=self._on_save).pack(anchor="w", pady=(16, 0))

    def on_show(self):
        """화면 진입 시 저장된 값을 불러와 채웁니다."""
        config = load_config()
        self.client_id.delete(0, "end")
        self.client_id.insert(0, config.get("spotify_client_id", ""))
        self.client_secret.delete(0, "end")
        self.client_secret.insert(0, config.get("spotify_client_secret", ""))
        self.status_label.configure(text="")

    def _on_save(self):
        client_id = self.client_id.get().strip()
        client_secret = self.client_secret.get().strip()
        save_config(client_id, client_secret)
        messagebox.showinfo("저장 완료", "설정이 저장되었습니다.")