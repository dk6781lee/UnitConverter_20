from boundary.boundary_error import BoundaryError
from boundary.input_validator import InputValidator
from boundary.output_formatter import OutputFormatter
from control.convert_use_case import ConvertUseCase
from entity.unit_registry import UnitRegistry


class GuiPresenter:
    def __init__(
        self,
        convert_use_case: ConvertUseCase,
        registry: UnitRegistry | None = None,
        validator: InputValidator | None = None,
        formatter: OutputFormatter | None = None,
    ) -> None:
        self._convert_use_case = convert_use_case
        self._validator = validator or InputValidator(registry=registry)
        self._formatter = formatter or OutputFormatter()

    def convert(self, input_text: str) -> tuple[str, str]:
        try:
            parsed = self._validator.validate(input_text)
            result = self._convert_use_case.execute(parsed)
            return self._formatter.format_text(result).rstrip("\n"), ""
        except BoundaryError as error:
            return "", error.message
