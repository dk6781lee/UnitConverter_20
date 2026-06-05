"""U-IN-01 · FR-01 valid parse — meter:2.5 (Boundary Track)."""

import pytest


def test_u_in_01_valid_parse_meter_2_5() -> None:
    # Given: stdin "meter:2.5"
    from boundary.cli_parser import CliParser

    stdin = "meter:2.5"

    # When: parse input
    parser = CliParser()
    result = parser.parse(stdin)

    # Then: unit=meter, value=2.5 (GREEN에서 assert)
    _ = result
    pytest.fail("RED: U-IN-01 — valid parse not implemented")
