from decimal import Decimal

from entity.domain_error import InvalidFactorError, UnknownUnitError


class UnitRegistry:
    def __init__(self) -> None:
        self._units: dict[str, Decimal] = {}

    def register(self, name: str, meters_per_unit: Decimal) -> None:
        if meters_per_unit <= 0:
            raise InvalidFactorError(name)
        self._units[name] = meters_per_unit

    def get_meters_per_unit(self, name: str) -> Decimal:
        if name not in self._units:
            raise UnknownUnitError(name)
        return self._units[name]

    def list_units(self) -> list[str]:
        return list(self._units.keys())

    def has_unit(self, name: str) -> bool:
        return name in self._units