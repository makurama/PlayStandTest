from dataclasses import dataclass
from typing import Optional, List, Dict
from decimal import Decimal


@dataclass
class NewsGet:
    start_date: Optional[str]
    finish_date: Optional[str]
    key_word: Optional[str]
    counter_news: Optional[int]
