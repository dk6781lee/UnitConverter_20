import sys
from pathlib import Path

_TESTS = Path(__file__).resolve().parent
_SRC = _TESTS.parent / "src"
for _path in (_SRC, _TESTS):
    _entry = str(_path)
    if _entry not in sys.path:
        sys.path.insert(0, _entry)
