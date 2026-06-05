from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ConversionLine:
    target_unit: str
    domain_value: Decimal


@dataclass(frozen=True)
class ConversionResult:
    source_unit: str
    source_value: Decimal
    lines: list[ConversionLine]
