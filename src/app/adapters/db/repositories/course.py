from sqlalchemy import select, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.entities.course import CourseEntity
from app.adapters.db.entities.currency import CurrencyEntity
from app.application.dto.course import CourseDtoOut, CourseDtoIn
from app.application.dto.currency import CurrencyDtoOut
from app.application.protocols.repositories.course import CourseRepositoryProtocol


class CourseRepository(CourseRepositoryProtocol):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_course_by_id(self, course_id: int) -> CourseDtoOut | None:
        course: CourseEntity | None = (
            await self.db.execute(
                select(CourseEntity)
                .where(CourseEntity.id == course_id)
            )
        ).scalar_one_or_none()

        left_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.id == course.left_currency_id)
            )
        ).scalar_one_or_none()

        if left_currency is None:
            return None

        right_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.id == course.right_currency_id)
            )
        ).scalar_one_or_none()

        if right_currency is None:
            return None

        return CourseDtoOut(
            id=course.id,
            left_currency=CurrencyDtoOut(
                id=left_currency.id,
                code=left_currency.code,
                name=left_currency.name,
                type=left_currency.type,
            ),
            right_currency=CurrencyDtoOut(
                id=right_currency.id,
                code=right_currency.code,
                name=right_currency.name,
                type=right_currency.type,
            ),
            course=course.course,
            date=course.date,
        )

    async def get_current_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoOut | None:
        left_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.code == left_currency_code)
            )
        ).scalar_one_or_none()

        if left_currency is None:
            return None

        right_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.code == right_currency_code)
            )
        ).scalar_one_or_none()

        if right_currency is None:
            return None

        course: CourseEntity | None = (
            await self.db.execute(
                select(CourseEntity)
                .where(
                    CourseEntity.left_currency_id == left_currency.id,
                    CourseEntity.right_currency_id == right_currency.id,
                )
                .order_by(desc(CourseEntity.date))
                .limit(1)
            )
        ).scalar_one_or_none()

        if course:
            return CourseDtoOut(
                id=course.id,
                left_currency=CurrencyDtoOut(
                    id=left_currency.id,
                    code=left_currency.code,
                    name=left_currency.name,
                    type=left_currency.type,
                ),
                right_currency=CurrencyDtoOut(
                    id=right_currency.id,
                    code=right_currency.code,
                    name=right_currency.name,
                    type=right_currency.type,
                ),
                course=course.course,
                date=course.date,
            )

        course = (
            await self.db.execute(
                select(CourseEntity)
                .where(
                    CourseEntity.left_currency_id == right_currency.id,
                    CourseEntity.right_currency_id == left_currency.id
                )
            )
        ).scalar_one_or_none()

        if course:
            return CourseDtoOut(
                id=course.id,
                left_currency=CurrencyDtoOut(
                    id=right_currency.id,
                    code=right_currency.code,
                    name=right_currency.name,
                    type=right_currency.type,
                ),
                right_currency=CurrencyDtoOut(
                    id=left_currency.id,
                    code=left_currency.code,
                    name=left_currency.name,
                    type=left_currency.type,
                ),
                course=course.course,
                date=course.date,
            )

    async def insert(self, course: CourseDtoIn) -> int | None:
        left_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.code == course.left_currency_code)
            )
        ).scalar_one_or_none()

        if left_currency is None:
            return None

        right_currency: CurrencyEntity = (
            await self.db.execute(
                select(CurrencyEntity)
                .where(CurrencyEntity.code == course.right_currency_code)
            )
        ).scalar_one_or_none()

        if right_currency is None:
            return None

        course_id: int | None = (
            await self.db.execute(
                insert(CourseEntity)
                .values(
                    course=course.course,
                    date=course.date,
                    left_currency_id=left_currency.id,
                    right_currency_id=right_currency.id
                )
                .returning(CourseEntity.id)
            )
        ).scalar_one_or_none()

        await self.db.commit()

        return course_id
