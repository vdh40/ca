from typing import Sequence

from app.application.dto.course import CourseDtoIn
from app.application.dto.currency import CurrencyDtoIn
from app.application.protocols.exchange import ExchangeProtocol


class BinanceAdapter(ExchangeProtocol):
    def get_all_currencies(self) -> Sequence[CurrencyDtoIn]:
        pass

    def get_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoIn:
        pass
