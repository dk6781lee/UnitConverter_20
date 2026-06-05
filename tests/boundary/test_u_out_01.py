"""U-OUT-01 · FR-02 TEXT snapshot — meter:2.5 (Boundary Track)."""

import pytest


def test_u_out_01_text_snapshot_meter_2_5() -> None:
    # Given: stdin "meter:2.5", ConvertUseCase mocked (Boundary Track)
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:2.5"
    mock_use_case = MagicMock()

    # When: CLI runs TEXT output (RG-04, POLICY-O01)
    app = CliApp(convert_use_case=mock_use_case)
    stdout, _stderr, _exit_code = app.run(stdin)

    # Then: AC-01 — stdout contains "2.5" meter, "8.2" feet, "2.7" yard (1 decimal)
    _ = stdout
    pytest.fail("RED: U-OUT-01 — TEXT snapshot not implemented")
