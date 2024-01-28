from dataclasses import dataclass
from typing import NewType, Literal, Any

CurrencyType = NewType("CurrencyType", Literal["crypto", "state"])


@dataclass
class Currency:
    id: int
    code: str
    name: str
    type: CurrencyType

    def __eq__(self, other: Any) -> bool:
        return self.code == other.code and self.name == other.name and self.type == other.type
