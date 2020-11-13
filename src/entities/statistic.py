from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


@dataclass
class Statistic:
    """
    dataclass from input data
    """
    start_date: Optional[str]
    finish_date: Optional[str]
    ready_date: [str]
