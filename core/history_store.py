import json
import uuid
from datetime import datetime
from pathlib import Path

HISTORY_DIR = Path.home() / ".blog_poster_app"
HISTORY_PATH = HISTORY_DIR / "history.json"


def _load_all() -> dict:
    """전체 기록(노래/코드 통합)을 불러옵니다."""
    if not HISTORY_PATH.exists():
        return {"song": [], "code": []}
    try:
        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            data.setdefault("song", [])
            data.setdefault("code", [])
            return data
    except (json.JSONDecodeError, OSError):
        return {"song": [], "code": []}


def _save_all(data: dict) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_history(kind: str) -> list:
    """kind: 'song' 또는 'code'. 최신순으로 반환합니다."""
    data = _load_all()
    entries = data.get(kind, [])
    return sorted(entries, key=lambda e: e["created_at"], reverse=True)


def add_entry(kind: str, title: str, inputs: dict, html: str) -> dict:
    """
    새 기록을 추가합니다.
    - title: 목록에 표시할 블로그 제목
    - inputs: 폼에 입력했던 값 전체 (재편집/재사용 대비)
    - html: 생성된 HTML
    """
    data = _load_all()
    entry = {
        "id": str(uuid.uuid4()),
        "title": title,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "inputs": inputs,
        "html": html,
    }
    data.setdefault(kind, []).append(entry)
    _save_all(data)
    return entry


def delete_entry(kind: str, entry_id: str) -> None:
    data = _load_all()
    data[kind] = [e for e in data.get(kind, []) if e["id"] != entry_id]
    _save_all(data)


def get_entry(kind: str, entry_id: str) -> dict | None:
    data = _load_all()
    for e in data.get(kind, []):
        if e["id"] == entry_id:
            return e
    return None