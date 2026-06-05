from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from boundary.gui.presenter import GuiPresenter


class MainWindow(QWidget):
    def __init__(self, presenter: GuiPresenter) -> None:
        super().__init__()
        self._presenter = presenter
        self.setWindowTitle("Unit Converter")

        self.unit_input = QLineEdit()
        self.unit_input.setPlaceholderText("unit")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("value")
        self.combined_input = QLineEdit()
        self.combined_input.setPlaceholderText("unit:value")
        self.convert_button = QPushButton("Convert")
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: red;")

        unit_row = QHBoxLayout()
        unit_row.addWidget(QLabel("Unit:"))
        unit_row.addWidget(self.unit_input)
        unit_row.addWidget(QLabel("Value:"))
        unit_row.addWidget(self.value_input)

        layout = QVBoxLayout()
        layout.addLayout(unit_row)
        layout.addWidget(self.combined_input)
        layout.addWidget(self.convert_button)
        layout.addWidget(QLabel("Results:"))
        layout.addWidget(self.result_area)
        layout.addWidget(self.error_label)
        self.setLayout(layout)

        self.convert_button.clicked.connect(self._on_convert)

    def _on_convert(self) -> None:
        combined = self.combined_input.text().strip()
        if combined:
            input_text = combined
        else:
            input_text = f"{self.unit_input.text().strip()}:{self.value_input.text().strip()}"

        result_text, error_text = self._presenter.convert(input_text)
        if error_text:
            self.result_area.clear()
            self.error_label.setText(error_text)
        else:
            self.error_label.clear()
            self.result_area.setPlainText(result_text)
