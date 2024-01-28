from dataclasses import dataclass
from datetime import datetime

from app.application.dto.currency import CurrencyDtoOut


@dataclass(frozen=True)
class CourseDtoIn:
    left_currency_code: str
    right_currency_code: str
    course: float
    date: datetime


@dataclass(frozen=True)
class CourseDtoOut:
    id: int
    left_currency: CurrencyDtoOut
    right_currency: CurrencyDtoOut
    course: float
    date: datetime
