"""D-CNV-03 · FR-04 negative · D-CNV-03b · FR-01 zero (Domain Track)."""

import pytest


def test_d_cnv_03_negative_quantity_rejected() -> None:
    # Given: negative numeric value
    from decimal import Decimal

    from entity.quantity import Quantity

    # When: create Quantity with -1
    Quantity.create(Decimal("-1"), "meter")

    # Then: DomainError (GREEN에서 assert)
    pytest.fail("RED: D-CNV-03 — negative Quantity not implemented")


def test_d_cnv_03b_zero_meter_conversion() -> None:
    # Given: Registry bootstrap, quantity = 0 meter
    from decimal import Decimal

    from entity.conversion_service import ConversionService
    from entity.quantity import Quantity
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("meter", Decimal("1"))
    registry.register("feet", Decimal("0.3048"))
    quantity = Quantity(Decimal("0"), "meter", registry)

    # When: convert zero to feet via hub
    service = ConversionService(registry)
    service.convert(quantity, "feet")

    # Then: 0 feet (GREEN에서 assert)
    pytest.fail("RED: D-CNV-03b — zero conversion not implemented")
