import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".blog_poster_app"
CONFIG_PATH = CONFIG_DIR / "config.json"


def load_config() -> dict:
    """설정을 불러옵니다. 파일이 없으면 빈 딕셔너리를 반환합니다."""
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(spotify_client_id: str, spotify_client_secret: str) -> None:
    """설정을 저장합니다."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    data = {
        "spotify_client_id": spotify_client_id,
        "spotify_client_secret": spotify_client_secret,
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def is_configured() -> bool:
    """Spotify 키가 설정되어 있는지 확인합니다."""
    config = load_config()
    return bool(config.get("spotify_client_id")) and bool(config.get("spotify_client_secret"))