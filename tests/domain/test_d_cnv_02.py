"""D-CNV-02 · FR-02 round-trip — feet → meter → feet (Domain Track)."""

from decimal import Decimal


def test_d_cnv_02_feet_round_trip() -> None:
    # Given: Registry with feet = 0.3048, quantity = 1 feet
    from entity.conversion_service import ConversionService
    from entity.quantity import Quantity
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("feet", Decimal("0.3048"))
    quantity = Quantity(Decimal("1"), "feet", registry)

    # When: hub round-trip feet → meter → feet
    service = ConversionService(registry)
    meters = service.to_meters(quantity)
    result = service.from_meters(meters, "feet")

    # Then: round-trip restores 1 feet
    assert result == Decimal("1")
