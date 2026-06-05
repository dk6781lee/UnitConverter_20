from decimal import ROUND_HALF_UP, Decimal

from control.conversion_result import ConversionResult


class OutputFormatter:
    def format_text(self, result: ConversionResult) -> str:
        lines = []
        source_display = self._format_source_value(result.source_value)
        for line in result.lines:
            display = self._format_display(line.domain_value)
            lines.append(
                f"{source_display} {result.source_unit} = {display} {line.target_unit}"
            )
        return "\n".join(lines) + "\n"

    def _format_display(self, value: Decimal) -> str:
        quantized = value.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        if quantized == 0:
            return "0.0"
        return format(quantized.normalize(), "f")

    def _format_source_value(self, value: Decimal) -> str:
        return format(value.normalize(), "f")
