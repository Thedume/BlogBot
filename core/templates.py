def format_song_post(track_info: dict, youtube_url: str, lyrics: str, impression: str) -> str:
    """J-POP 노래 소개 티스토리 HTML 템플릿을 반환합니다.
    track_info, youtube_url은 없을 수 있으므로 조건부로 섹션을 구성합니다.
    """
    album_image_url = track_info.get("album_image", "")
    artist = track_info.get("artist", "")

    image_section = ""
    if album_image_url:
        image_section = f'<p>[##_Image|{album_image_url}|CDM|1.3|{{"originWidth":340,"originHeight":336,"style":"alignCenter","caption":"{track_info.get("album", "")}"}}_##]</p>\n'

    info_section = ""
    if track_info.get("name"):
        info_section = (
            f'<p data-ke-size="size16">🎶&nbsp;노래&nbsp;정보 <br />'
            f'-&nbsp;곡명&nbsp;: {track_info["name"]}<br />'
            f'-&nbsp;아티스트&nbsp;: {track_info["artist"]}<br />'
            f'-&nbsp;앨범명&nbsp;/&nbsp;발매일&nbsp;: {track_info["album"]} / {track_info["release_date"]}<br />'
            f'-&nbsp;장르&nbsp;:&nbsp;#JPOP #노래추천</p>\n<p data-ke-size="size16">&nbsp;</p>\n'
        )

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


def build_song_title(jp_title: str, kr_title: str, artist: str) -> str:
    """블로그 제목 조합 로직 (기존 SongModal.on_submit 내부 로직 이식)"""
    if jp_title and artist:
        return f"{jp_title}({kr_title}) - {artist}"
    return f"({kr_title})"


def build_code_title(language: str, problem_title: str) -> str:
    """블로그 제목 조합 로직 (기존 CodeModal.on_submit 내부 로직 이식)"""
    return f"[{language.strip()}] {problem_title.strip()}"