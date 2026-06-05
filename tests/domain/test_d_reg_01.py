"""D-REG-01 · NFR-01 inch add · D-REG-01b · factor>0 (Domain Track)."""

import pytest
from decimal import Decimal


def test_d_reg_01_inch_register_ocp() -> None:
    # Given: bootstrap Registry, inch meters_per_unit = 0.0254
    from entity.conversion_service import ConversionService
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("meter", Decimal("1"))
    registry.register("feet", Decimal("0.3048"))

    # When: register inch (OCP — ConversionService diff 0)
    registry.register("inch", Decimal("0.0254"))
    service = ConversionService(registry)
    _ = service

    # Then: inch in list_units; core converter unchanged
    assert "inch" in registry.list_units()


def test_d_reg_01b_zero_factor_rejected() -> None:
    # Given: empty Registry
    from entity.domain_error import DomainError
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()

    # When / Then: register unit with zero meters_per_unit → DomainError
    with pytest.raises(DomainError):
        registry.register("bad", Decimal("0"))

    assert registry.list_units() == []
