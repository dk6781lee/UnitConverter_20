from decimal import Decimal, InvalidOperation

from boundary.boundary_error import BoundaryError, E001_MESSAGE, E002_TEMPLATE
from control.parsed_input import ParsedInput


class CliParser:
    def parse(self, stdin: str) -> ParsedInput:
        text = stdin.strip()
        if ":" not in text:
            raise BoundaryError(1, E001_MESSAGE)

        unit, value_token = text.split(":", 1)
        if not unit or not value_token:
            raise BoundaryError(1, E001_MESSAGE)

        try:
            value = Decimal(value_token)
        except InvalidOperation:
            raise BoundaryError(2, E002_TEMPLATE.format(token=value_token)) from None

        return ParsedInput(unit=unit, value=value)
