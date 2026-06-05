"""D-CFG-01a/b/c · EXT-01 config load · fail-fast (Data Track)."""

import pytest


def test_d_cfg_01a_valid_config_load() -> None:
    # Given: valid config/units.json with inch entry
    from pathlib import Path

    from data.json_unit_ratio_source import JsonUnitRatioSource

    config_path = Path("config/units.json")

    # When: load unit ratios
    source = JsonUnitRatioSource(config_path)
    ratios = source.load()

    # Then: meter, feet, yard (+ inch if extended) loaded (GREEN에서 assert)
    _ = ratios
    pytest.fail("RED: D-CFG-01a — valid config load not implemented")


def test_d_cfg_01b_missing_config_e005() -> None:
    # Given: non-existent config path
    from pathlib import Path

    from data.json_unit_ratio_source import JsonUnitRatioSource

    missing = Path("config/does_not_exist.json")

    # When: load missing file
    source = JsonUnitRatioSource(missing)
    source.load()

    # Then: LoadError → E005, no 3-unit fallback (GREEN에서 assert)
    pytest.fail("RED: D-CFG-01b — missing config fail-fast not implemented")


def test_d_cfg_01c_zero_factor_e005() -> None:
    # Given: temp config with meters_per_unit = 0
    import json
    import tempfile
    from pathlib import Path

    from data.json_unit_ratio_source import JsonUnitRatioSource

    payload = {
        "$schema": "unitconverter/units-v1",
        "units": [{"name": "meter", "meters_per_unit": "0"}],
    }
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        temp_path = Path(f.name)

    # When: load invalid schema
    source = JsonUnitRatioSource(temp_path)
    source.load()

    # Then: LoadError → E005 (GREEN에서 assert)
    pytest.fail("RED: D-CFG-01c — zero factor schema reject not implemented")
