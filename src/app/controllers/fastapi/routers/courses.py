from fastapi import (
    APIRouter,
    status, Depends, Query,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.database import get_db
from app.application.services.course import CourseService

router = APIRouter(prefix="/courses")


@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
async def get_current_course(
        left_currency_code: str = Query(),
        right_currency_code: str = Query(),
        db_session: AsyncSession = Depends(get_db)
):
    return await CourseService(db_session).get_current_course(left_currency_code=left_currency_code,
                                                              right_currency_code=right_currency_code)
