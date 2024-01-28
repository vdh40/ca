from contextlib import contextmanager
from datetime import datetime
from typing import Sequence

from requests import Session

from app.application.dto.course import CourseDtoIn
from app.application.dto.currency import CurrencyDtoIn
from app.application.protocols.exchange import ExchangeProtocol
from app.core.config import config


class CoingeckoAdapter(ExchangeProtocol):
    def get_all_currencies(self) -> Sequence[CurrencyDtoIn]:
        with self._get_requests_session() as session:
            coins_response = session.get("{}/coins/list".format(config.exchanges.coingecko_url)).json()

            coins = [
                CurrencyDtoIn(code=coin.get("symbol"), name=coin.get("name"), type="crypto")
                for coin in coins_response
            ]

            currencies_response = session.get(
                "{}/simple/supported_vs_currencies".format(config.exchanges.coingecko_url)
            ).json()

            currencies = [
                CurrencyDtoIn(code=currency, name=currency, type="state")
                for currency in currencies_response
            ]

            return [*coins, *currencies]

    def get_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoIn:
        with self._get_requests_session() as session:
            course = session.get(
                "{}/simple/price".format(config.exchanges.coingecko_url),
                params={"ids": left_currency_code, "vs_currencies": right_currency_code}
            ).json()

            return CourseDtoIn(
                left_currency_code=left_currency_code,
                right_currency_code=right_currency_code,
                course=course.get(left_currency_code).get(right_currency_code),
                date=datetime.now(),
            )

    @contextmanager
    def _get_requests_session(self):
        session: Session = Session()

        try:
            yield session
        finally:
            session.close()
