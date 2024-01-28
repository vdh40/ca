from typing import Sequence

from app.adapters.exchange.binance import BinanceAdapter
from app.adapters.exchange.coingecko import CoingeckoAdapter
from app.application.dto.course import CourseDtoIn
from app.application.dto.currency import CurrencyDtoIn
from app.application.protocols.exchange import ExchangeProtocol


class Exchange(ExchangeProtocol):
    def __init__(self):
        self.binance: BinanceAdapter = BinanceAdapter()
        self.coingecko: CoingeckoAdapter = CoingeckoAdapter()

    def get_currency_by_code(self, code: str) -> CurrencyDtoIn:
        pass

    def get_all_currencies(self) -> Sequence[CurrencyDtoIn]:
        # here should be balancing between binance and coingecko
        return self.coingecko.get_all_currencies()

    def get_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoIn:
        # here should be balancing between binance and coingecko
        return self.coingecko.get_course(left_currency_code, right_currency_code)
