import customtkinter as ctk

from gui.main_screen import MainScreen
from gui.song_form import SongFormScreen
from gui.code_form import CodeFormScreen
from gui.result_screen import ResultScreen


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("블로그 포스팅 생성기")
        self.geometry("720x640")
        self.minsize(600, 500)

        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("blue")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.screens = {}
        for ScreenClass in (MainScreen, SongFormScreen, CodeFormScreen, ResultScreen):
            screen = ScreenClass(container, self)
            self.screens[ScreenClass.__name__] = screen
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_screen("MainScreen")

    def show_screen(self, name: str):
        self.screens[name].tkraise()

    def show_result(self, kind: str, blog_title: str, html: str, inputs: dict, return_screen: str, save_to_history: bool = True):
        self.screens["ResultScreen"].show_result(kind, blog_title, html, inputs, return_screen, save_to_history)


def run_app():
    app = App()
    app.mainloop()