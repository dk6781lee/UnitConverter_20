import os
from pathlib import Path

_GOLDEN_DIR = Path(__file__).resolve().parent / "golden"


def assert_matches_golden(actual: str, relative: str) -> None:
    approved_path = _GOLDEN_DIR / relative

    if os.environ.get("UPDATE_GOLDEN") == "1":
        approved_path.parent.mkdir(parents=True, exist_ok=True)
        approved_path.write_text(actual, encoding="utf-8")
        return

    if not approved_path.exists():
        raise AssertionError(
            f"Golden file missing: {approved_path}. "
            "Run with UPDATE_GOLDEN=1 to create."
        )

    expected = approved_path.read_text(encoding="utf-8")
    if actual != expected:
        raise AssertionError(
            f"Golden mismatch: {relative}\n"
            f"--- expected ({len(expected)} chars) ---\n"
            f"{expected}"
            f"--- actual ({len(actual)} chars) ---\n"
            f"{actual}"
        )
