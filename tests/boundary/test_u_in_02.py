"""U-IN-02a/b/c · FR-05 format · number errors (Boundary Track)."""

import pytest

from boundary.boundary_error import BoundaryError, E001_MESSAGE, E002_TEMPLATE
from boundary.input_validator import InputValidator


def test_u_in_02a_missing_colon_e001() -> None:
    # Given: stdin "meter" (no colon)
    stdin = "meter"

    # When: validate input
    validator = InputValidator()
    with pytest.raises(BoundaryError) as exc_info:
        validator.validate(stdin)

    # Then: E001 exit 1
    assert exc_info.value.exit_code == 1
    assert exc_info.value.message == E001_MESSAGE


def test_u_in_02b_invalid_decimal_e002() -> None:
    # Given: stdin "meter:2.5.3"
    stdin = "meter:2.5.3"

    # When: validate input
    validator = InputValidator()
    with pytest.raises(BoundaryError) as exc_info:
        validator.validate(stdin)

    # Then: E002 exit 2, token=2.5.3
    assert exc_info.value.exit_code == 2
    assert exc_info.value.message == E002_TEMPLATE.format(token="2.5.3")


def test_u_in_02c_alpha_value_e002() -> None:
    # Given: stdin "meter:abc"
    stdin = "meter:abc"

    # When: validate input
    validator = InputValidator()
    with pytest.raises(BoundaryError) as exc_info:
        validator.validate(stdin)

    # Then: E002 exit 2, token=abc
    assert exc_info.value.exit_code == 2
    assert exc_info.value.message == E002_TEMPLATE.format(token="abc")
