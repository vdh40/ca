from typing import Protocol, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.currency import CurrencyDtoOut, CurrencyDtoIn


class CurrencyRepositoryProtocol(Protocol):
    db: AsyncSession

    async def get_currency_by_code(self, code: str) -> CurrencyDtoOut:
        pass

    async def bulk_insert(self, currencies_data: Sequence[CurrencyDtoIn]) -> None:
        pass
