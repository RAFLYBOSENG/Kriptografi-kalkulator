from pathlib import Path


class Config:
    SECRET_KEY = "dev-secret-key"
    INSTANCE_PATH = Path(__file__).resolve().parent.parent / "instance"
    HISTORY_PATH = INSTANCE_PATH / "history.json"
