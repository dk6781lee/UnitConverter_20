"""U-IN-03a/b/c · FR-03 unknown · FR-04 negative · FR-01 zero (Boundary Track)."""

from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from boundary.boundary_error import BoundaryError, E003_TEMPLATE, E004_TEMPLATE
from boundary.cli_app import CliApp
from boundary.input_validator import InputValidator
from control.conversion_result import ConversionLine, ConversionResult
from control.registry_bootstrap import load_registry_from_config


def _bootstrap_registry():
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    return load_registry_from_config(config_path)


def test_u_in_03a_unknown_unit_e003() -> None:
    # Given: stdin "cubit:1", ConvertUseCase mocked
    stdin = "cubit:1"
    mock_use_case = MagicMock()
    registry = _bootstrap_registry()

    # When: run CLI
    app = CliApp(convert_use_case=mock_use_case, registry=registry)
    stdout, stderr, exit_code = app.run(stdin)

    # Then: E003 exit 3, stderr Unknown unit: cubit
    assert exit_code == 3
    assert stderr == E003_TEMPLATE.format(unit="cubit") + "\n"
    assert stdout == ""
    mock_use_case.execute.assert_not_called()


def test_u_in_03b_negative_value_e004() -> None:
    # Given: stdin "meter:-1"
    stdin = "meter:-1"

    # When: validate input
    validator = InputValidator()
    with pytest.raises(BoundaryError) as exc_info:
        validator.validate(stdin)

    # Then: E004 exit 4, stderr Negative value not allowed: -1
    assert exc_info.value.exit_code == 4
    assert exc_info.value.message == E004_TEMPLATE.format(value=Decimal("-1"))


def test_u_in_03c_zero_meter_ok() -> None:
    # Given: stdin "meter:0", ConvertUseCase mocked
    stdin = "meter:0"
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = ConversionResult(
        source_unit="meter",
        source_value=Decimal("0"),
        lines=[
            ConversionLine("meter", Decimal("0")),
            ConversionLine("feet", Decimal("0")),
            ConversionLine("yard", Decimal("0")),
        ],
    )
    registry = _bootstrap_registry()

    # When: run CLI
    app = CliApp(convert_use_case=mock_use_case, registry=registry)
    stdout, stderr, exit_code = app.run(stdin)

    # Then: exit 0, stdout contains 0 meter = 0.0 feet
    assert exit_code == 0
    assert stderr == ""
    assert "0 meter = 0.0 feet" in stdout
    mock_use_case.execute.assert_called_once()
