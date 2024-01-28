from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from app.adapters.db.database import BaseEntity
from app.adapters.db.entities.currency import CurrencyEntity


class CourseEntity(BaseEntity):
    __tablename__ = "course"

    left_currency_id: Mapped[int] = mapped_column(ForeignKey(CurrencyEntity.id))
    right_currency_id: Mapped[int] = mapped_column(ForeignKey(CurrencyEntity.id))
    course: Mapped[float] = mapped_column()
    date: Mapped[datetime] = mapped_column()
