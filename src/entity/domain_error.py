class DomainError(Exception):
    pass


class NegativeValueError(DomainError):
    pass


class InvalidFactorError(DomainError):
    pass


class UnknownUnitError(DomainError):
    def __init__(self, unit: str) -> None:
        self.unit = unit
        super().__init__(unit)
