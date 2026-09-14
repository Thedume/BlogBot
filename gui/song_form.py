import customtkinter as ctk
from tkinter import messagebox

from core.spotify_client import fetch_track_info, SpotifyNotConfiguredError
from core.templates import format_song_post, build_song_title
from gui.widgets import ResizableTextbox


class SongFormScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=24, pady=24)

        ctk.CTkLabel(scroll, text="노래 소개 작성", font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w", pady=(0, 16))

        self.spotify_link = self._add_entry(scroll, "Spotify 링크 (선택)", "https://open.spotify.com/track/...")
        self.youtube_link = self._add_entry(scroll, "YouTube 링크 (선택)", "https://youtu.be/...")
        self.title_kr = self._add_entry(scroll, "제목 한국어 해석 (선택)", "예: 아이돌")
        self.artist = self._add_entry(scroll, "아티스트 (선택)", "미입력 시 Spotify 정보로 자동 채워집니다")

        ctk.CTkLabel(scroll, text="가사 (원어/발음/번역)", anchor="w").pack(fill="x", pady=(12, 4))
        self.lyrics = ResizableTextbox(scroll, height=120)
        self.lyrics.pack(fill="x")

        ctk.CTkLabel(scroll, text="감상평", anchor="w").pack(fill="x", pady=(12, 4))
        self.impression = ResizableTextbox(scroll, height=80)
        self.impression.pack(fill="x")

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

    def _add_entry(self, parent, label_text, placeholder):
        ctk.CTkLabel(parent, text=label_text, anchor="w").pack(fill="x", pady=(4, 4))
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder)
        entry.pack(fill="x")
        return entry

    def _on_reset(self):
        self.spotify_link.delete(0, "end")
        self.youtube_link.delete(0, "end")
        self.title_kr.delete(0, "end")
        self.artist.delete(0, "end")
        self.lyrics.clear()
        self.impression.clear()
        self.error_label.configure(text="")

    def _on_submit(self):
        self.error_label.configure(text="")
        title_kr = self.title_kr.get().strip()
        artist_manual = self.artist.get().strip()
        lyrics = self.lyrics.get().strip()
        impression = self.impression.get().strip()

        if not lyrics:
            self.error_label.configure(text="가사를 입력해주세요.")
            return
        if len(impression) < 10:
            self.error_label.configure(text="감상평을 10자 이상 입력해주세요.")
            return

        spotify_url = self.spotify_link.get().strip()
        youtube_url = self.youtube_link.get().strip()

        track_info = {}
        if spotify_url:
            try:
                track_info = fetch_track_info(spotify_url)
            except SpotifyNotConfiguredError:
                messagebox.showerror("설정 필요", "Spotify API 키가 설정되지 않았습니다. 설정 화면에서 입력해주세요.")
                return
            except Exception as e:
                messagebox.showerror("오류", f"Spotify에서 곡 정보를 가져오지 못했습니다.\n링크를 확인해 주세요.\n\n{e}")
                return

        # 아티스트 우선순위: 직접 입력 > Spotify 값
        effective_artist = artist_manual if artist_manual else track_info.get("artist", "")

        blog_title = build_song_title(track_info.get("name", ""), title_kr, effective_artist)
        html = format_song_post(track_info, youtube_url, lyrics, impression, title_kr=title_kr, manual_artist=artist_manual)

        inputs = {
            "spotify_link": spotify_url,
            "youtube_link": youtube_url,
            "title_kr": title_kr,
            "artist": artist_manual,
            "lyrics": lyrics,
            "impression": impression,
        }

        self.controller.show_result(
            kind="song",
            blog_title=blog_title,
            html=html,
            inputs=inputs,
            return_screen="SongFormScreen",
        )

    def load_inputs(self, inputs: dict):
        """기록에서 '불러오기'로 진입 시 폼에 값을 채웁니다."""
        self.spotify_link.delete(0, "end")
        self.spotify_link.insert(0, inputs.get("spotify_link", ""))
        self.youtube_link.delete(0, "end")
        self.youtube_link.insert(0, inputs.get("youtube_link", ""))
        self.title_kr.delete(0, "end")
        self.title_kr.insert(0, inputs.get("title_kr", ""))
        self.artist.delete(0, "end")
        self.artist.insert(0, inputs.get("artist", ""))
        self.lyrics.set(inputs.get("lyrics", ""))
        self.impression.set(inputs.get("impression", ""))
        self.error_label.configure(text="")