from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.course import CourseDtoOut, CourseDtoIn


class CourseRepositoryProtocol(Protocol):
    db: AsyncSession

    async def get_course_by_id(self, entity_id: int) -> CourseDtoOut | None:
        pass

    async def get_current_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoOut | None:
        pass

    async def insert(self, course: CourseDtoIn) -> int | None:
        pass
