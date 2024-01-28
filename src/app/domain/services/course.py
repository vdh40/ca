from datetime import datetime

from app.domain.models.currency import Currency
from app.domain.models.course import Course


class CourseDomainService:
    @staticmethod
    def create_course(id_: int, right_currency: Currency, left_currency: Currency, course: float, date: datetime) -> Course:
        return Course(id=id_, right_currency=right_currency, left_currency=left_currency, course=course, date=date)

    @staticmethod
    def revert_course(course: Course) -> Course:
        source_right_currency = course.right_currency
        course.right_currency = course.left_currency
        course.left_currency = source_right_currency

        course.course = 1 / course.course

        return course
