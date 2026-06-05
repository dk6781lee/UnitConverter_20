---
description: TDD RED 스켈레톤 — tests/만, pytest.fail 또는 import 실패, pytest FAIL 확인
---

# RED Skeleton — 실패 테스트 껍데기

UnitConverter_20 **RED Phase 구현** — `tests/`에 **스켈레톤 1건** 작성 후 **pytest FAIL** 확인.  
**근거:** `.cursorrules` · `docs/PRD.md` §10 · `/red-test-plan` 산출물(있으면)

**선행:** `/red-test-plan` (선택) · Harness (`pyproject.toml`, `tests/`, `config/units.json`)

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: red | Layer: entity|control|boundary|data | Track: Domain|Boundary|Data | Target: D-*|U-*
```

---

## 목적 (Objective)

- Target Test ID에 맞는 **pytest 스켈레톤 1건**을 `tests/`에 작성한다.
- **의도적 FAIL** — `pytest.fail("RED: …")` **또는** `src/` 미구현으로 **import 실패**.
- `src/`, `UnitConverter.py`, `config/`는 **수정하지 않는다**.
- GREEN·REFACTOR는 **하지 않는다**.

---

## Track · Layer · 파일 매핑

| Track | Layer | 테스트 경로 | Mock |
|-------|-------|-------------|------|
| **Domain** | entity, control | `tests/domain/test_d_*.py` | Domain Mock **금지** |
| **Boundary** | boundary | `tests/boundary/test_u_*.py` | `ConvertUseCase` 등 Mock **허용** |
| **Data** | data | `tests/data/test_d_cfg_*.py` | temp files only |

---

## 스켈레톤 규칙

1. **AAA 주석** — `# Given:` · `# When:` · `# Then:` (3단계)
2. **Then 처리 (택1)**
   - `pytest.fail("RED: {Test ID} — {reason}")` — GREEN 전까지 도달 가능 시
   - `from entity…` / `from boundary…` import — **미구현 시 `ModuleNotFoundError` = 정상 RED**
3. **금지:** assert 본문 · 통과 더미 · `@pytest.mark.skip` · `xfail` · `pytest.importorskip`
4. **Domain Track:** `unittest.mock`, `@patch`, `MagicMock` on Registry·ConversionService **금지**
5. **Boundary Track:** Mock은 Given에만; Then은 `pytest.fail` 또는 stderr/exit assert **스켈레톤 단계에서는 assert 본문 없음**

### Domain 예시 (D-CNV-01)

```python
"""D-CNV-01 · FR-02 hub conversion — 1 feet → meter (Domain Track)."""

import pytest


def test_d_cnv_01_feet_to_meters_hub() -> None:
    # Given: Registry feet = 0.3048, quantity = 1 feet
    from decimal import Decimal

    from entity.conversion_service import ConversionService
    from entity.quantity import Quantity
    from entity.unit_registry import UnitRegistry

    registry = UnitRegistry()
    registry.register("feet", Decimal("0.3048"))
    quantity = Quantity(Decimal("1"), "feet", registry)

    # When: hub conversion to meters
    service = ConversionService(registry)
    service.to_meters(quantity)

    # Then: 0.3048 ±1e-9 (GREEN에서 assert)
    pytest.fail("RED: D-CNV-01 — feet to meters not implemented")
```

### Boundary 예시 (U-OUT-01)

```python
"""U-OUT-01 · FR-02 TEXT snapshot — meter:2.5 (Boundary Track)."""

import pytest


def test_u_out_01_text_snapshot_meter_2_5() -> None:
    # Given: stdin "meter:2.5", ConvertUseCase mocked
    from unittest.mock import MagicMock

    from boundary.cli_app import CliApp

    stdin = "meter:2.5"
    mock_use_case = MagicMock()

    # When: CLI TEXT output (RG-04, POLICY-O01)
    app = CliApp(convert_use_case=mock_use_case)
    stdout, _stderr, _exit_code = app.run(stdin)

    # Then: AC-01 — "2.5" meter, "8.2" feet, "2.7" yard
    _ = stdout
    pytest.fail("RED: U-OUT-01 — TEXT snapshot not implemented")
```

---

## 수행 절차 (Steps)

1. **Target 확정** — 사용자 지정 또는 `/red-test-plan` 표.
2. **Phase 선언** — 필수 선언 형식 출력.
3. **파일 1개 작성** — `tests/{domain|boundary|data}/test_*.py` (Target 1건).
4. **`src/` 미수정** 확인.
5. **pytest 단일 실행** — Target 파일 또는 함수 1개.
6. **FAIL 확인** — `FAILED` 필수. `PASSED`면 스켈레톤·더미 재검토.
7. **보고** — 아래 형식. **GREEN 하지 않음.**

---

## pytest 예시

```bash
# Domain — Windows PowerShell
python -m pytest tests/domain/test_d_cnv_01.py -v

# Boundary
python -m pytest tests/boundary/test_u_out_01.py -v

# Data
python -m pytest tests/data/test_d_cfg_01.py -v

# 단일 함수
python -m pytest tests/domain/test_d_cnv_01.py::test_d_cnv_01_feet_to_meters_hub -q
```

**정상 RED 출력 예:**

```text
FAILED … — ModuleNotFoundError: No module named 'entity.conversion_service'
```

또는

```text
FAILED … — Failed: RED: D-CNV-01 — feet to meters not implemented
```

---

## Skeleton 완료 보고

```markdown
## RED Skeleton 완료

- Target: D-CNV-01
- pytest: FAILED — ModuleNotFoundError: No module named 'entity.conversion_service'
- 변경 파일: tests/domain/test_d_cnv_01.py (tests/만)
- Mock: Domain Track — 없음
- src/: 무변경
- 다음: /green-minimal — src/entity 최소 구현 (green 브랜치)
```

---

## 성공 조건

- [ ] Target 테스트 **1개**만 추가·수정
- [ ] AAA 주석 (Given / When / Then)
- [ ] `pytest` 결과 = **FAILED**
- [ ] 변경 = **`tests/`만**
- [ ] assert 본문 · skip · xfail · 통과 더미 **없음**
- [ ] `src/` **무변경**

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **`src/` · `UnitConverter.py` · `config/` 수정** | RED = tests/만 |
| **assert 본문** (스켈레톤 단계) | GREEN에서 작성 |
| **통과 더미** (`pass`, `assert True`) | RED 우회 |
| **Domain Track Mock** | Dual-Track 규칙 |
| **skip / xfail / importorskip** | merge gate 위반 |
| **한 턴에 여러 Target** | 1 FAIL = 1 RED |
| **GREEN / REFACTOR** | 순서 위반 |
| **git commit** | 사용자 요청 시만 |
