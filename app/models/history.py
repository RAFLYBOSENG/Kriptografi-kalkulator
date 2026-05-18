from dataclasses import dataclass
from datetime import datetime


@dataclass
class HistoryItem:
    algorithm: str
    mode: str
    input_text: str
    output_text: str
    created_at: datetime
