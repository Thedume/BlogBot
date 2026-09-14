import customtkinter as ctk


class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        wrapper = ctk.CTkFrame(self, fg_color="transparent")
        wrapper.place(relx=0.5, rely=0.4, anchor="center")

        title = ctk.CTkLabel(wrapper, text="블로그 포스팅 생성기", font=ctk.CTkFont(size=20, weight="bold"))
        title.pack(pady=(0, 24))

        button_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        button_row.pack()

        ctk.CTkButton(
            button_row, text="노래 소개", width=140, height=64,
            command=lambda: controller.show_screen("SongFormScreen")
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            button_row, text="코딩 테스트", width=140, height=64,
            command=lambda: controller.show_screen("CodeFormScreen")
        ).pack(side="left", padx=8)

        bottom_row = ctk.CTkFrame(wrapper, fg_color="transparent")
        bottom_row.pack(pady=(20, 0))

        # 기록 보기 / 설정 화면은 이후 단계에서 만들고 여기에 연결합니다.
        ctk.CTkButton(
            bottom_row, text="기록 보기", width=100, height=28,
            fg_color="transparent", text_color=("gray20", "gray80"),
            hover_color=("gray90", "gray30")
        ).pack(side="left", padx=6)

        ctk.CTkButton(
            bottom_row, text="설정", width=100, height=28,
            fg_color="transparent", text_color=("gray20", "gray80"),
            hover_color=("gray90", "gray30")
        ).pack(side="left", padx=6)