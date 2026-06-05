"""U-OUT-01b · EXT-03 JSON output — meter:2.5 (Boundary Track)."""

import pytest


def test_u_out_01b_json_snapshot_meter_2_5() -> None:
    # Given: stdin "meter:2.5", --format json, ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:2.5"
    mock_use_case = MagicMock()

    # When: CLI runs JSON output
    app = CliApp(convert_use_case=mock_use_case)
    stdout, _stderr, _exit_code = app.run(stdin, output_format="json")

    # Then: §6.2 JSON schema — display 8.2 feet, 2.7 yard (GREEN에서 assert)
    _ = stdout
    pytest.fail("RED: U-OUT-01b — JSON output not implemented")
