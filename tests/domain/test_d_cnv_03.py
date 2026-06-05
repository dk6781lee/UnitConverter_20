"""D-CNV-03 · FR-04 negative · D-CNV-03b · FR-01 zero (Domain Track)."""

import pytest
from decimal import Decimal


def test_d_cnv_03_negative_quantity_rejected() -> None:
    # Given: negative numeric value
    from entity.domain_error import DomainError
    from entity.quantity import Quantity

    # When / Then: create Quantity with -1 → DomainError
    with pytest.raises(DomainError):
        Quantity.create(Decimal("-1"), "meter")


def test_d_cnv_03b_zero_meter_conversion() -> None:
    # Given: Registry bootstrap, quantity = 0 meter
    from entity.conversion_service import ConversionService
    from entity.quantity import Quantity
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("meter", Decimal("1"))
    registry.register("feet", Decimal("0.3048"))
    quantity = Quantity(Decimal("0"), "meter", registry)

    # When: convert zero to feet via hub
    service = ConversionService(registry)
    result = service.convert(quantity, "feet")

    # Then: 0 feet
    assert result == Decimal("0")
