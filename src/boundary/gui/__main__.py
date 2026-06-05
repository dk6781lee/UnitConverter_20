import sys
from pathlib import Path

from PyQt6.QtWidgets import QApplication

from boundary.gui.main_window import MainWindow
from boundary.gui.presenter import GuiPresenter
from control.convert_use_case import ConvertUseCase
from control.registry_bootstrap import load_registry_from_config
from entity.conversion_service import ConversionService


def main() -> None:
    config_path = Path(__file__).resolve().parents[3] / "config" / "units.json"
    registry = load_registry_from_config(config_path)
    conversion_service = ConversionService(registry)
    use_case = ConvertUseCase(registry, conversion_service)
    presenter = GuiPresenter(convert_use_case=use_case, registry=registry)

    app = QApplication(sys.argv)
    window = MainWindow(presenter=presenter)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
