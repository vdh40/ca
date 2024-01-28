from app.domain.models.currency import Currency, CurrencyType


class CurrencyDomainService:
    @staticmethod
    def create_currency(id_: int, code: str, name: str, currency_type: CurrencyType) -> Currency:
        return Currency(id=id_, code=code, name=name, type=currency_type)
