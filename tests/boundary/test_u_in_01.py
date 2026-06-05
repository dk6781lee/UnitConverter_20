"""U-IN-01 · FR-01 valid parse — meter:2.5 (Boundary Track)."""

from decimal import Decimal


def test_u_in_01_valid_parse_meter_2_5() -> None:
    # Given: stdin "meter:2.5"
    from boundary.cli_parser import CliParser

    stdin = "meter:2.5"

    # When: parse input
    parser = CliParser()
    result = parser.parse(stdin)

    # Then: unit=meter, value=2.5
    assert result.unit == "meter"
    assert result.value == Decimal("2.5")
