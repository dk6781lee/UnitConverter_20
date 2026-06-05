from boundary.boundary_error import BoundaryError, E003_TEMPLATE, E004_TEMPLATE
from boundary.cli_parser import CliParser
from control.parsed_input import ParsedInput
from entity.unit_registry import UnitRegistry


class InputValidator:
    def __init__(self, registry: UnitRegistry | None = None) -> None:
        self._parser = CliParser()
        self._registry = registry

    def validate(self, stdin: str) -> ParsedInput:
        parsed = self._parser.parse(stdin.strip())

        if parsed.value < 0:
            raise BoundaryError(4, E004_TEMPLATE.format(value=parsed.value))

        if self._registry is not None and not self._registry.has_unit(parsed.unit):
            raise BoundaryError(3, E003_TEMPLATE.format(unit=parsed.unit))

        return parsed
