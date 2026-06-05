"""U-OUT-01 · FR-02 TEXT snapshot — meter:2.5 (Boundary Track)."""

from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

from boundary.cli_app import CliApp
from control.conversion_result import ConversionLine, ConversionResult
from control.convert_use_case import ConvertUseCase
from control.registry_bootstrap import load_registry_from_config
from entity.conversion_service import ConversionService

_GOLDEN_U_OUT_01 = "u_out_01_meter_2_5.approved.txt"


def _bootstrap_registry():
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    return load_registry_from_config(config_path)


def test_u_out_01_text_snapshot_meter_2_5() -> None:
    # Given: stdin "meter:2.5", ConvertUseCase mocked (Boundary Track)
    from _approval import assert_matches_golden

    stdin = "meter:2.5"
    mock_use_case = MagicMock()
    mock_use_case.execute.return_value = ConversionResult(
        source_unit="meter",
        source_value=Decimal("2.5"),
        lines=[
            ConversionLine("meter", Decimal("2.5")),
            ConversionLine("feet", Decimal("8.2021")),
            ConversionLine("yard", Decimal("2.734025")),
        ],
    )
    registry = _bootstrap_registry()

    # When: CLI runs TEXT output (RG-04, POLICY-O01)
    app = CliApp(convert_use_case=mock_use_case, registry=registry)
    stdout, stderr, exit_code = app.run(stdin)

    # Then: AC-01 — stdout golden master (PRD §6.1)
    assert exit_code == 0
    assert stderr == ""
    assert_matches_golden(stdout, _GOLDEN_U_OUT_01)
    mock_use_case.execute.assert_called_once()


def test_u_out_01_integration_smoke_meter_2_5() -> None:
    # Given: real stack — no Domain Mock
    from _approval import assert_matches_golden

    registry = _bootstrap_registry()
    use_case = ConvertUseCase(registry, ConversionService(registry))
    app = CliApp(convert_use_case=use_case, registry=registry)

    # When: CLI runs TEXT output end-to-end
    stdout, stderr, exit_code = app.run("meter:2.5")

    # Then: AC-01 snapshot via real ConversionService — same golden
    assert exit_code == 0
    assert stderr == ""
    assert_matches_golden(stdout, _GOLDEN_U_OUT_01)
