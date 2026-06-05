from boundary.parsed_input import ParsedInput
from control.conversion_result import ConversionLine, ConversionResult
from entity.conversion_service import ConversionService
from entity.quantity import Quantity
from entity.unit_registry import UnitRegistry


class ConvertUseCase:
    def __init__(
        self,
        registry: UnitRegistry,
        conversion_service: ConversionService,
    ) -> None:
        self._registry = registry
        self._conversion_service = conversion_service

    def execute(self, parsed: ParsedInput) -> ConversionResult:
        quantity = Quantity(parsed.value, parsed.unit, self._registry)
        lines = [
            ConversionLine(
                target_unit=unit,
                domain_value=self._conversion_service.convert(quantity, unit),
            )
            for unit in self._registry.list_units()
        ]
        return ConversionResult(
            source_unit=parsed.unit,
            source_value=parsed.value,
            lines=lines,
        )
