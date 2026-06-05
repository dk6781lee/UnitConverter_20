"""U-IN-02a/b/c · FR-05 format · number errors (Boundary Track)."""

import pytest


def test_u_in_02a_missing_colon_e001() -> None:
    # Given: stdin "meter" (no colon)
    from boundary.input_validator import InputValidator

    stdin = "meter"

    # When: validate input
    validator = InputValidator()
    validator.validate(stdin)

    # Then: E001 exit 1 (GREEN에서 assert)
    pytest.fail("RED: U-IN-02a — format error not implemented")


def test_u_in_02b_invalid_decimal_e002() -> None:
    # Given: stdin "meter:2.5.3"
    from boundary.input_validator import InputValidator

    stdin = "meter:2.5.3"

    # When: validate input
    validator = InputValidator()
    validator.validate(stdin)

    # Then: E002 exit 2, token=2.5.3 (GREEN에서 assert)
    pytest.fail("RED: U-IN-02b — decimal parse error not implemented")


def test_u_in_02c_alpha_value_e002() -> None:
    # Given: stdin "meter:abc"
    from boundary.input_validator import InputValidator

    stdin = "meter:abc"

    # When: validate input
    validator = InputValidator()
    validator.validate(stdin)

    # Then: E002 exit 2, token=abc (GREEN에서 assert)
    pytest.fail("RED: U-IN-02c — alpha number error not implemented")
