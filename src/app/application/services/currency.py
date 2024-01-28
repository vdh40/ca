from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.repositories.currency import CurrencyRepository
from app.adapters.exchange.exchange import Exchange
from app.application.dto.currency import CurrencyDtoOut, CurrencyDtoIn
from app.application.protocols.exchange import ExchangeProtocol
from app.application.protocols.repositories.currency import CurrencyRepositoryProtocol


class CurrencyService:
    def __init__(self, db: AsyncSession):
        # Should be injected via DI
        self.repository: CurrencyRepositoryProtocol = CurrencyRepository(db)
        # Should be injected via DI
        self.exchange: ExchangeProtocol = Exchange()

    async def get_currency_by_code(self, code: str) -> CurrencyDtoOut:
        return await self.repository.get_currency_by_code(code)

    async def import_all_currencies(self) -> None:
        currencies: Sequence[CurrencyDtoIn] = self.exchange.get_all_currencies()
        await self.repository.bulk_insert(currencies)
