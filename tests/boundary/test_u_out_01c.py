"""U-OUT-01c · EXT-03 CSV output — meter:2.5 (Boundary Track)."""

import pytest


def test_u_out_01c_csv_snapshot_meter_2_5() -> None:
    # Given: stdin "meter:2.5", --format csv, ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:2.5"
    mock_use_case = MagicMock()

    # When: CLI runs CSV output
    app = CliApp(convert_use_case=mock_use_case)
    stdout, _stderr, _exit_code = app.run(stdin, output_format="csv")

    # Then: §6.3 CSV header + rows, display 8.2 feet (GREEN에서 assert)
    _ = stdout
    pytest.fail("RED: U-OUT-01c — CSV output not implemented")
