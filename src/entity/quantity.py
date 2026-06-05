from decimal import Decimal

from entity.domain_error import NegativeValueError
from entity.unit_registry import UnitRegistry


class Quantity:
    def __init__(self, value: Decimal, unit: str, registry: UnitRegistry) -> None:
        self.value = value
        self.unit = unit
        self._registry = registry

    @classmethod
    def create(
        cls,
        value: Decimal,
        unit: str,
        registry: UnitRegistry | None = None,
    ) -> "Quantity":
        if value < 0:
            raise NegativeValueError()
        if registry is None:
            raise TypeError("registry is required for non-negative quantities")
        return cls(value, unit, registry)