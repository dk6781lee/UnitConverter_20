import json
from decimal import Decimal
from pathlib import Path

from entity.unit_registry import UnitRegistry


def load_registry_from_config(config_path: Path) -> UnitRegistry:
    data = json.loads(config_path.read_text(encoding="utf-8"))
    registry = UnitRegistry()
    for unit in data["units"]:
        registry.register(unit["name"], Decimal(unit["meters_per_unit"]))
    return registry
