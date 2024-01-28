from fastapi import (
    APIRouter,
    status,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.database import get_db
from app.application.services.currency import CurrencyService

router = APIRouter(prefix="/currencies")


@router.post(
    "/import",
    status_code=status.HTTP_200_OK,
)
async def import_currencies(
        db_session: AsyncSession = Depends(get_db)
):
    await CurrencyService(db_session).import_all_currencies()
