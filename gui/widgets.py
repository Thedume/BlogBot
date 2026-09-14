import customtkinter as ctk


class ResizableTextbox(ctk.CTkFrame):
    """
    CTkTextbox + 우측 하단 리사이즈 핸들.
    핸들을 마우스로 드래그하면 텍스트박스 높이가 늘어나거나 줄어듭니다.
    """

    def __init__(self, parent, height=90, min_height=60, max_height=500, **kwargs):
        super().__init__(parent, fg_color="transparent")
        self._height = height
        self._min_height = min_height
        self._max_height = max_height

        self.textbox = ctk.CTkTextbox(self, height=self._height, **kwargs)
        self.textbox.pack(fill="both", expand=True)

        grip = ctk.CTkLabel(
            self, text="⋰", cursor="sizing",
            fg_color=("gray85", "gray25"), width=16, height=12,
            text_color=("gray40", "gray60")
        )
        grip.place(relx=1.0, rely=1.0, anchor="se")
        grip.bind("<B1-Motion>", self._on_drag)

    def _on_drag(self, event):
        new_height = max(self._min_height, min(self._max_height, self._height + event.y))
        if new_height != self._height:
            self._height = new_height
            self.textbox.configure(height=self._height)

    def get(self) -> str:
        return self.textbox.get("1.0", "end-1c")

    def set(self, text: str):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text or "")

    def clear(self):
        self.textbox.delete("1.0", "end")