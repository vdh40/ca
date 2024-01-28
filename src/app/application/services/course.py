from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.repositories.course import CourseRepository
from app.adapters.exchange.exchange import Exchange
from app.application.dto.course import CourseDtoOut, CourseDtoIn
from app.application.protocols.exchange import ExchangeProtocol
from app.application.protocols.repositories.course import CourseRepositoryProtocol
from app.domain.models.course import Course
from app.domain.services.course import CourseDomainService


class CourseService:
    def __init__(self, db: AsyncSession):
        # should be injected via DI
        self.repository: CourseRepositoryProtocol = CourseRepository(db)
        # Should be injected via DI
        self.exchange: ExchangeProtocol = Exchange()

    async def get_current_course(self, left_currency_code: str, right_currency_code: str) -> CourseDtoOut:
        course: CourseDtoOut | None = await self.repository.get_current_course(left_currency_code, right_currency_code)

        if course:
            if course.left_currency.code != left_currency_code:
                reverted_course: Course = CourseDomainService.revert_course(Course(**course.__dict__))
                return CourseDtoOut(**reverted_course.__dict__)

            return course

        course_from_exchange: CourseDtoIn | None = self.exchange.get_course(left_currency_code, right_currency_code)

        if course_from_exchange:
            course_id: int | None = await self.repository.insert(course_from_exchange)

            if course_id:
                return await self.repository.get_course_by_id(course_id)
