import io
import os
import sys
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# =============================================
# 1. 환경변수 로드
#    - 로컬: .env 파일에서 자동으로 읽어옴
#    - Railway 등 배포 환경: 플랫폼의 환경변수 설정에서 읽어옴
# =============================================
load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
SPOTIPY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

# GUILD_ID: 로컬 개발 시 즉시 커맨드 동기화용. 배포 환경에서는 설정 안 해도 됨.
# .env에 GUILD_ID=123456789 형식으로 추가하면 됩니다.
_guild_id_str = os.getenv("GUILD_ID")
GUILD_ID = int(_guild_id_str) if _guild_id_str else None

# 필수 환경변수 누락 시 명확한 오류 메시지와 함께 종료
_missing = [k for k, v in {
    "DISCORD_TOKEN": TOKEN,
    "SPOTIFY_CLIENT_ID": SPOTIPY_CLIENT_ID,
    "SPOTIFY_CLIENT_SECRET": SPOTIPY_CLIENT_SECRET,
}.items() if not v]

if _missing:
    print(f"[오류] 다음 환경변수가 설정되지 않았습니다: {', '.join(_missing)}")
    print("로컬 실행 시 .env 파일을 확인하세요. 배포 환경이라면 플랫폼 환경변수를 확인하세요.")
    sys.exit(1)

# =============================================
# 2. Spotify 연결
# =============================================
auth_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(auth_manager=auth_manager)


# =============================================
# 3. 봇 클래스
# =============================================
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents.default())

    async def setup_hook(self):
        if GUILD_ID:
            # 특정 길드에만 즉시 동기화 (개발용)
            guild = discord.Object(id=GUILD_ID)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
            print(f"[봇] 슬래시 커맨드를 길드 {GUILD_ID}에 즉시 동기화했습니다.")
        else:
            # 전역 동기화 (프로덕션용, 반영까지 최대 1시간)
            await self.tree.sync()
            print("[봇] 슬래시 커맨드를 전역 동기화했습니다.")


bot = MyBot()


# =============================================
# 4. 템플릿 가공 함수
# =============================================

def format_song_post(track_info: dict, youtube_url: str, lyrics: str, impression: str) -> str:
    """J-POP 노래 소개 티스토리 HTML 템플릿을 반환합니다.
    track_info, youtube_url은 없을 수 있으므로 조건부로 섹션을 구성합니다.
    """
    album_image_url = track_info.get("album_image", "")
    artist = track_info.get("artist", "")

    # 앨범 이미지 섹션 (Spotify 정보 있을 때만)
    image_section = ""
    if album_image_url:
        image_section = f'<p>[##_Image|{album_image_url}|CDM|1.3|{{"originWidth":340,"originHeight":336,"style":"alignCenter","caption":"{track_info.get("album", "")}"}}_##]</p>\n'

    # 곡 정보 섹션 (Spotify 정보 있을 때만)
    info_section = ""
    if track_info.get("name"):
        info_section = (
            f'<p data-ke-size="size16">🎶&nbsp;노래&nbsp;정보 <br />'
            f'-&nbsp;곡명&nbsp;: {track_info["name"]}<br />'
            f'-&nbsp;아티스트&nbsp;: {track_info["artist"]}<br />'
            f'-&nbsp;앨범명&nbsp;/&nbsp;발매일&nbsp;: {track_info["album"]} / {track_info["release_date"]}<br />'
            f'-&nbsp;장르&nbsp;:&nbsp;#JPOP #노래추천</p>\n<p data-ke-size="size16">&nbsp;</p>\n'
        )

    # 듣기 링크 섹션 (있는 것만 포함)
    listen_lines = []
    if youtube_url:
        listen_lines.append(f'-&nbsp;YouTube:&nbsp;<a href="{youtube_url}">{youtube_url}</a>')
    if track_info.get("spotify_url"):
        listen_lines.append(f'-&nbsp;Spotify:&nbsp;<a href="{track_info["spotify_url"]}">{track_info["spotify_url"]}</a>')

    listen_section = ""
    if listen_lines:
        listen_section = (
            '<p data-ke-size="size16">🎧&nbsp;노래&nbsp;듣기 <br />'
            + '<br />'.join(listen_lines)
            + '<br /><br /></p>\n'
        )

    tag_artist = f'&nbsp;#{artist}' if artist else ''

    return (
        image_section
        + info_section
        + listen_section
        + f'<p data-ke-size="size16">🎶&nbsp;가사</p>\n'
        + f'<pre class="bash" data-ke-language="bash" data-ke-type="codeblock"><code>{lyrics}</code></pre>\n'
        + f'<p data-ke-size="size16"><br /><br />💬&nbsp;감상평 <br />{impression} <br /><br /><br />'
        + f'📌&nbsp;태그 <br />#노래추천&nbsp;#가사해석&nbsp;#음악공유&nbsp;#JPOP{tag_artist}</p>\n'
    )


def format_code_post(title: str, problem_body: str, solution_text: str, code: str) -> str:
    """코딩 테스트 풀이 티스토리 HTML 템플릿을 반환합니다."""
    return f"""<hr contenteditable="false" data-ke-type="horizontalRule" data-ke-style="style8" />
<ul style="list-style-type: disc;" data-ke-list-type="disc">
<li style="list-style-type: disc;" data-ke-style="style2"><b>문제: {title}</b></li>
</ul>
<p data-ke-size="size16">{problem_body}</p>
<ul style="list-style-type: disc;" data-ke-list-type="disc">
<li style="list-style-type: disc;" data-ke-style="style2"><b>풀이</b></li>
</ul>
<p data-ke-size="size16">{solution_text}</p>
<ul style="list-style-type: disc;" data-ke-list-type="disc">
<li style="list-style-type: disc;"><b>코드 확인</b></li>
</ul>
<div data-text-less="닫기" data-text-more="더보기" data-ke-type="moreLess"><a class="btn-toggle-moreless">더보기</a>
<div class="moreless-content">
<pre class="cpp" data-ke-language="cpp" data-ke-type="codeblock"><code>{code}</code></pre>
</div>
</div>
<p data-ke-size="size18">훈수는 언제나 환영입니다</p>
"""


# =============================================
# 5. 공통 유틸: HTML을 파일로 전송
# =============================================

async def send_as_file(interaction: discord.Interaction, html: str, filename: str):
    """
    생성된 HTML을 Discord 2000자 제한 없이 파일 첨부로 전송합니다.
    ephemeral=True이므로 본인에게만 보입니다.
    """
    buf = io.BytesIO(html.encode("utf-8"))
    file = discord.File(buf, filename=filename)
    await interaction.response.send_message(
        "✅ 아래 파일을 다운로드해서 티스토리 HTML 모드에 붙여넣으세요!",
        file=file,
        ephemeral=True
    )


# =============================================
# 6. 모달 정의
# =============================================

class SongModal(discord.ui.Modal, title='J-POP 노래 소개 작성'):
    spotify_link = discord.ui.TextInput(
        label='Spotify 곡 링크 (선택)',
        placeholder='https://open.spotify.com/track/...',
        required=False
    )
    youtube_link = discord.ui.TextInput(
        label='YouTube 링크 (선택)',
        placeholder='https://youtu.be/...',
        required=False
    )
    title_kr = discord.ui.TextInput(
        label='제목 한국어 해석',
        placeholder='예: 아이돌  (블로그 제목에 사용됩니다)',
    )
    lyrics = discord.ui.TextInput(
        label='가사 (원문/발음/번역)',
        style=discord.TextStyle.paragraph,
        placeholder='일어\n발음\n번역 순으로 작성해주세요.'
    )
    impression = discord.ui.TextInput(
        label='감상평',
        style=discord.TextStyle.paragraph,
        min_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):
        track_info = {}
        spotify_url_value = self.spotify_link.value.strip()

        # Spotify 링크가 있을 때만 API 호출
        if spotify_url_value:
            try:
                track = sp.track(spotify_url_value)
                images = track['album'].get('images', [])
                track_info = {
                    "name": track['name'],
                    "artist": track['artists'][0]['name'],
                    "album": track['album']['name'],
                    "release_date": track['album']['release_date'],
                    "spotify_url": track['external_urls']['spotify'],
                    "album_image": images[0]['url'] if images else "",
                }
            except Exception as e:
                await interaction.response.send_message(
                    f"❌ Spotify에서 곡 정보를 가져오지 못했습니다.\n링크를 확인해 주세요.\n```{e}```",
                    ephemeral=True
                )
                return

        # 블로그 제목 메시지 구성: 일본어제목(한국어해석) - 가수명
        jp_title = track_info.get("name", "")
        artist   = track_info.get("artist", "")
        if jp_title and artist:
            blog_title = f"{jp_title}({self.title_kr.value}) - {artist}"
        else:
            blog_title = f"({self.title_kr.value})"

        html = format_song_post(
            track_info,
            self.youtube_link.value.strip(),
            self.lyrics.value,
            self.impression.value
        )

        buf = io.BytesIO(html.encode("utf-8"))
        file = discord.File(buf, filename="song_post.html")
        await interaction.response.send_message(
            f"📝 **블로그 제목**\n```\n{blog_title}\n```\n✅ 아래 파일을 다운로드해서 티스토리 HTML 모드에 붙여넣으세요!",
            file=file,
            ephemeral=True
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(
            f"❌ 예상치 못한 오류가 발생했습니다.\n```{error}```",
            ephemeral=True
        )


class CodeModal(discord.ui.Modal, title='코딩 테스트 풀이 작성'):
    language = discord.ui.TextInput(
        label='사용 언어',
        placeholder='예: C++  /  Python  /  Java',
        max_length=20
    )
    # ✅ 'title' → 'problem_title': Modal.title 속성과 이름 충돌 방지
    problem_title = discord.ui.TextInput(
        label='문제 번호 + 제목',
        placeholder='예: 백준 1000번 - A+B'
    )
    problem = discord.ui.TextInput(
        label='문제 설명 + 예제 입출력',
        style=discord.TextStyle.paragraph,
        placeholder='문제 설명을 적고, 아래에 예제 입력/출력도 함께 적어주세요.'
    )
    solution = discord.ui.TextInput(
        label='풀이 설명',
        style=discord.TextStyle.paragraph
    )
    code = discord.ui.TextInput(
        label='코드',
        style=discord.TextStyle.paragraph
    )

    async def on_submit(self, interaction: discord.Interaction):
        # 블로그 제목 메시지 구성: [사용언어] 백준 1000번 - A+B
        blog_title = f"[{self.language.value.strip()}] {self.problem_title.value.strip()}"

        html = format_code_post(
            self.problem_title.value,
            self.problem.value,
            self.solution.value,
            self.code.value
        )

        buf = io.BytesIO(html.encode("utf-8"))
        file = discord.File(buf, filename="code_post.html")
        await interaction.response.send_message(
            f"📝 **블로그 제목**\n```\n{blog_title}\n```\n✅ 아래 파일을 다운로드해서 티스토리 HTML 모드에 붙여넣으세요!",
            file=file,
            ephemeral=True
        )

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message(
            f"❌ 예상치 못한 오류가 발생했습니다.\n```{error}```",
            ephemeral=True
        )


# =============================================
# 7. 슬래시 커맨드 등록
# =============================================

@bot.tree.command(name="포스팅", description="블로그 포스팅 초안을 생성합니다.")
@app_commands.choices(종류=[
    app_commands.Choice(name="노래 소개 (J-POP)", value="song"),
    app_commands.Choice(name="코딩 테스트", value="code")
])
async def posting(interaction: discord.Interaction, 종류: app_commands.Choice[str]):
    if 종류.value == "song":
        await interaction.response.send_modal(SongModal())
    else:
        await interaction.response.send_modal(CodeModal())


# =============================================
# 8. 봇 실행
# =============================================
bot.run(TOKEN)