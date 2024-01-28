from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.config import config

engine = create_async_engine(
    str(config.db.url)
)


class BaseEntity(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)

    metadata = MetaData(schema=config.db.schema_name)


Session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db: AsyncSession = Session()

    try:
        yield db
    finally:
        await db.close()
