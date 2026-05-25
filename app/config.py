import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    SITE_NAME = os.environ.get("SITE_NAME", "CipherLab")
    SITE_URL = os.environ.get("SITE_URL", "https://kriptografly.my.id")
    SITE_DESCRIPTION = os.environ.get(
        "SITE_DESCRIPTION",
        "Belajar kriptografi klasik dengan Caesar, Vigenere, Affine, Hill, dan Playfair secara interaktif.",
    )
    INSTANCE_PATH = Path(__file__).resolve().parent.parent / "instance"
    HISTORY_PATH = INSTANCE_PATH / "history.json"
