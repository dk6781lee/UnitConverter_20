"""U-IN-03a/b/c · FR-03 unknown · FR-04 negative · FR-01 zero (Boundary Track)."""

import pytest


def test_u_in_03a_unknown_unit_e003() -> None:
    # Given: stdin "cubit:1", ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "cubit:1"
    mock_use_case = MagicMock()

    # When: run CLI
    app = CliApp(convert_use_case=mock_use_case)
    _stdout, stderr, exit_code = app.run(stdin)

    # Then: E003 exit 3, stderr Unknown unit: cubit (GREEN에서 assert)
    _ = stderr, exit_code
    pytest.fail("RED: U-IN-03a — unknown unit not implemented")


def test_u_in_03b_negative_value_e004() -> None:
    # Given: stdin "meter:-1"
    from boundary.input_validator import InputValidator

    stdin = "meter:-1"

    # When: validate input
    validator = InputValidator()
    validator.validate(stdin)

    # Then: E004 exit 4, stderr Negative value not allowed: -1 (GREEN에서 assert)
    pytest.fail("RED: U-IN-03b — negative value reject not implemented")


def test_u_in_03c_zero_meter_ok() -> None:
    # Given: stdin "meter:0", ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:0"
    mock_use_case = MagicMock()

    # When: run CLI
    app = CliApp(convert_use_case=mock_use_case)
    stdout, _stderr, exit_code = app.run(stdin)

    # Then: exit 0, stdout contains 0 meter = 0.0 feet (GREEN에서 assert)
    _ = stdout, exit_code
    pytest.fail("RED: U-IN-03c — zero input ok not implemented")
