from decimal import Decimal

from entity.quantity import Quantity
from entity.unit_registry import UnitRegistry


class ConversionService:
    def __init__(self, registry: UnitRegistry) -> None:
        self._registry = registry

    def to_meters(self, quantity: Quantity) -> Decimal:
        meters_per_unit = self._registry.get_meters_per_unit(quantity.unit)
        return quantity.value * meters_per_unit

    def convert(self, quantity: Quantity, target_unit: str) -> Decimal:
        meters = self.to_meters(quantity)
        return self.from_meters(meters, target_unit)

    def from_meters(self, meters: Decimal, target_unit: str) -> Decimal:
        target_ratio = self._registry.get_meters_per_unit(target_unit)
        return meters / target_ratio
