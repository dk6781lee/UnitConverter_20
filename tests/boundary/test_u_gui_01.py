"""U-GUI-01 · EXT-04 PyQt GUI — meter:2.5 → feet 8.2, yard 2.7 (Boundary Track)."""

from decimal import Decimal
from pathlib import Path
from unittest.mock import MagicMock

from PyQt6.QtCore import Qt

from boundary.gui.main_window import MainWindow
from boundary.gui.presenter import GuiPresenter
from control.conversion_result import ConversionLine, ConversionResult
from control.convert_use_case import ConvertUseCase
from control.registry_bootstrap import load_registry_from_config
from entity.conversion_service import ConversionService


def _bootstrap_registry():
    config_path = Path(__file__).resolve().parents[2] / "config" / "units.json"
    return load_registry_from_config(config_path)


def _assert_rg04_results(result_text: str) -> None:
    assert "8.2 feet" in result_text
    assert "2.7 yard" in result_text
    assert "2.5 meter = 2.5 meter" in result_text


def test_u_gui_01_convert_meter_2_5_mock(qtbot) -> None:
    # Given: unit=meter, value=2.5, ConvertUseCase mocked (Boundary Track)
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
    presenter = GuiPresenter(convert_use_case=mock_use_case, registry=registry)
    window = MainWindow(presenter=presenter)
    qtbot.addWidget(window)

    # When: user clicks Convert
    window.unit_input.setText("meter")
    window.value_input.setText("2.5")
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)

    # Then: RG-04 + POLICY-O01 in result area; no error
    result_text = window.result_area.toPlainText()
    assert window.error_label.text() == ""
    _assert_rg04_results(result_text)
    mock_use_case.execute.assert_called_once()


def test_u_gui_01_convert_meter_2_5_integration(qtbot) -> None:
    # Given: real stack — no Domain Mock
    registry = _bootstrap_registry()
    use_case = ConvertUseCase(registry, ConversionService(registry))
    presenter = GuiPresenter(convert_use_case=use_case, registry=registry)
    window = MainWindow(presenter=presenter)
    qtbot.addWidget(window)

    # When: user clicks Convert
    window.unit_input.setText("meter")
    window.value_input.setText("2.5")
    qtbot.mouseClick(window.convert_button, Qt.MouseButton.LeftButton)

    # Then: same RG-04 display as U-OUT-01 AC-01
    result_text = window.result_area.toPlainText()
    assert window.error_label.text() == ""
    _assert_rg04_results(result_text)
