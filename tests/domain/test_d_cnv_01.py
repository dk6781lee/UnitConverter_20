"""D-CNV-01 · FR-02 hub conversion — 1 feet → meter (Domain Track)."""

import pytest


def test_d_cnv_01_feet_to_meters_hub() -> None:
    # Given: Registry with feet meters_per_unit = 0.3048, quantity = 1 feet
    from decimal import Decimal

    from entity.conversion_service import ConversionService
    from entity.quantity import Quantity
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("feet", Decimal("0.3048"))
    quantity = Quantity(Decimal("1"), "feet", registry)

    # When: hub conversion to meters
    service = ConversionService(registry)
    service.to_meters(quantity)

    # Then: 0.3048 ±1e-9 (GREEN에서 assert)
    pytest.fail("RED: D-CNV-01 — feet to meters not implemented")
