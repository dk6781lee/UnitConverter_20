"""U-OUT-02 · EXT-03 invalid format — --format xml → E007 (Boundary Track)."""

import pytest


def test_u_out_02_invalid_format_e007() -> None:
    # Given: stdin "meter:2.5", --format xml, ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:2.5"
    mock_use_case = MagicMock()

    # When: CLI runs with invalid output format
    app = CliApp(convert_use_case=mock_use_case)
    _stdout, stderr, exit_code = app.run(stdin, output_format="xml")

    # Then: E007 exit 7, stderr Invalid output format: xml (GREEN에서 assert)
    _ = stderr, exit_code
    pytest.fail("RED: U-OUT-02 — invalid format error not implemented")
