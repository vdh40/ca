from dataclasses import dataclass
from datetime import datetime

from app.domain.models.currency import Currency


@dataclass
class Course:
    id: int
    left_currency: Currency
    right_currency: Currency
    course: float
    date: datetime
