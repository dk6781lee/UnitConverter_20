from boundary.boundary_error import BoundaryError
from boundary.input_validator import InputValidator
from boundary.output_formatter import OutputFormatter
from control.convert_use_case import ConvertUseCase
from entity.unit_registry import UnitRegistry


class CliApp:
    def __init__(
        self,
        convert_use_case: ConvertUseCase,
        registry: UnitRegistry | None = None,
        validator: InputValidator | None = None,
        formatter: OutputFormatter | None = None,
    ) -> None:
        self._convert_use_case = convert_use_case
        self._registry = registry
        self._validator = validator or InputValidator(registry=registry)
        self._formatter = formatter or OutputFormatter()

    def run(self, stdin: str) -> tuple[str, str, int]:
        try:
            parsed = self._validator.validate(stdin)
            result = self._convert_use_case.execute(parsed)
            stdout = self._formatter.format_text(result)
            return stdout, "", 0
        except BoundaryError as error:
            return "", error.message + "\n", error.exit_code
