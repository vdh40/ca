from typing import Sequence

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.entities.currency import CurrencyEntity
from app.application.dto.currency import CurrencyDtoOut, CurrencyDtoIn
from app.application.protocols.repositories.currency import CurrencyRepositoryProtocol
from app.core.utils import batch


class CurrencyRepository(CurrencyRepositoryProtocol):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_currency_by_code(self, code: str) -> CurrencyDtoOut:
        currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.code == code)
            )
        ).scalar_one()

        return CurrencyDtoOut(
            id=currency.id,
            code=currency.code,
            name=currency.name,
            type=currency.type,
        )

    async def bulk_insert(self, currencies_data: Sequence[CurrencyDtoIn]) -> None:
        currencies = [currency.__dict__ for currency in currencies_data]

        for currencies_batch in batch(currencies, 10000):
            await self.db.execute(insert(CurrencyEntity).values(currencies_batch).on_conflict_do_nothing())

        await self.db.commit()
