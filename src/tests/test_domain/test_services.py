import datetime

from app.domain.models.course import Course
from app.domain.models.currency import Currency
from app.domain.services.course import CourseDomainService
from app.domain.services.currency import CurrencyDomainService


class TestCurrencyService:
    def test_create_currency(self):
        currency: Currency = CurrencyDomainService.create_currency(id_=1, code="USD", name="USA Dollar", currency_type="state")

        assert currency.id == 1
        assert currency.code == "USD"
        assert currency.name == "USA Dollar"
        assert currency.type == "state"


class TestCourseService:
    def test_create_course(self):
        left_currency: Currency = Currency(
            id=1,
            code="BTC",
            name="Bitcoin",
            type="crypto",
        )

        right_currency: Currency = Currency(
            id=2,
            code="USD",
            name="USA Dollar",
            type="state",
        )

        course_date: datetime = datetime.datetime.now()

        course: Course = CourseDomainService.create_course(
            id_=1,
            left_currency=left_currency,
            right_currency=right_currency,
            course=1.534,
            date=course_date,
        )

        assert course.id == 1
        assert course.left_currency == left_currency
        assert course.right_currency == right_currency
        assert course.course == 1.534
        assert course.date == course_date

    def test_revert_course(self):
        left_currency: Currency = Currency(
            id=1,
            code="BTC",
            name="Bitcoin",
            type="crypto",
        )

        right_currency: Currency = Currency(
            id=2,
            code="USD",
            name="USA Dollar",
            type="state",
        )

        course_date: datetime = datetime.datetime.now()

        course_value: float = 1.534

        course: Course = Course(
            id=1,
            left_currency=left_currency,
            right_currency=right_currency,
            course=course_value,
            date=course_date,
        )

        reverted_course: Course = CourseDomainService.revert_course(
            course=course,
        )

        assert reverted_course.id == 1
        assert reverted_course.left_currency == right_currency
        assert reverted_course.right_currency == left_currency
        assert reverted_course.course == 1. / course_value
        assert reverted_course.date == course_date
