import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from core.config_store import load_config


class SpotifyNotConfiguredError(Exception):
    """Spotify API 키가 설정되지 않았을 때 발생합니다."""
    pass


def get_spotify_client() -> spotipy.Spotify:
    """설정에 저장된 키로 Spotify 클라이언트를 생성합니다."""
    config = load_config()
    client_id = config.get("spotify_client_id")
    client_secret = config.get("spotify_client_secret")

    if not client_id or not client_secret:
        raise SpotifyNotConfiguredError("Spotify API 키가 설정되지 않았습니다. 설정 화면에서 입력해주세요.")

    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    return spotipy.Spotify(auth_manager=auth_manager)


def fetch_track_info(spotify_url: str) -> dict:
    """
    Spotify 트랙 링크로 곡 정보를 조회합니다.
    기존 SongModal.on_submit()의 조회 로직과 동일합니다.

    반환 형식:
    {
        "name": str, "artist": str, "album": str,
        "release_date": str, "spotify_url": str, "album_image": str
    }

    실패 시 spotipy 예외가 그대로 위로 전파됩니다 (GUI 쪽에서 잡아서 에러 메시지 표시).
    """
    sp = get_spotify_client()
    track = sp.track(spotify_url)
    images = track['album'].get('images', [])
    return {
        "name": track['name'],
        "artist": track['artists'][0]['name'],
        "album": track['album']['name'],
        "release_date": track['album']['release_date'],
        "spotify_url": track['external_urls']['spotify'],
        "album_image": images[0]['url'] if images else "",
    }