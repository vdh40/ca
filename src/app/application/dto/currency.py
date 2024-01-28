from dataclasses import dataclass
from typing import NewType, Literal

from app.domain.models.currency import CurrencyType


@dataclass(frozen=True)
class CurrencyDtoIn:
    code: str
    name: str
    type: CurrencyType


@dataclass(frozen=True)
class CurrencyDtoOut:
    id: int
    code: str
    name: str
    type: CurrencyType
