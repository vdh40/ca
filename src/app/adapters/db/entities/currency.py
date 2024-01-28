from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.adapters.db.database import BaseEntity
from app.domain.models.currency import CurrencyType


class CurrencyEntity(BaseEntity):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    type: Mapped[CurrencyType] = mapped_column(String)
