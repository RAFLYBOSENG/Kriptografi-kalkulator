import json
from datetime import datetime
from pathlib import Path


_HISTORY_PATH = Path(__file__).resolve().parents[2] / 'instance' / 'history.json'


def load_history():
    try:
        if not _HISTORY_PATH.exists():
            return []
        with _HISTORY_PATH.open('r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def save_history(entry):
    """Save a history entry and attach a timestamp.

    Entry is a dict that should contain at least: algorithm, mode, text, result
    """
    data = load_history()
    # add readable timestamp
    try:
        entry = dict(entry)
        entry.setdefault('time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    except Exception:
        pass
    data.append(entry)
    try:
        _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _HISTORY_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return entry


def clear_history():
    try:
        _HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _HISTORY_PATH.open('w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return []
