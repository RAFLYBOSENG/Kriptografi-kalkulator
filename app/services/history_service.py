import json
from pathlib import Path


_HISTORY_PATH = Path('instance') / 'history.json'


def load_history():
    try:
        if not _HISTORY_PATH.exists():
            return []
        with _HISTORY_PATH.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history(entry):
    data = load_history()
    data.append(entry)
    try:
        _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _HISTORY_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return entry
