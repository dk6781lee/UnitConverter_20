from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class ParsedInput:
    unit: str
    value: Decimal
