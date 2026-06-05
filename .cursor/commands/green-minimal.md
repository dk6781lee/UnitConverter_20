---
description: TDD GREEN — RED Target 1건 최소 구현, pytest.fail 제거, PASS 확인 (green 브랜치)
---

# GREEN Minimal — 최소 구현으로 RED 해소

UnitConverter_20 **BCE + Dual-Track TDD** — **GREEN 단계만** 수행한다.  
**근거:** `.cursorrules` · `docs/PRD.md` §10 · `docs/TODO.md`  
**선행:** `red` 브랜치 RED 스켈레톤 · `green` 브랜치 checkout

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: green | Layer: entity|control|boundary|data | Track: Domain|Boundary|Data | Target: D-*|U-*
```

---

## 목적 (Objective)

- RED에서 **의도적 FAIL** 중인 **Target Test ID 1건**을 PASS시킨다.
- `src/`에 **해당 Target에 필요한 최소 코드만** 추가·수정한다.
- `tests/`에서 `pytest.fail("RED: …")` 제거 → PRD 계약 **엄격 assert**로 교체.
- REFACTOR·EXT·무관 Target 동시 구현은 **하지 않는다**.

---

## Track · Layer · 구현 매핑

| Track | Layer | 테스트 경로 | 구현 위치 | Mock |
|-------|-------|-------------|-----------|------|
| **Domain** | entity (+ control 최소) | `tests/domain/test_d_*.py` | `src/entity/` | Domain Mock **금지** |
| **Boundary** | boundary (+ control) | `tests/boundary/test_u_*.py` | `src/boundary/`, `src/control/` | Service Mock **허용** |
| **Data** | data (+ control) | `tests/data/test_d_cfg_*.py` | `src/data/` | temp files only |

**Assert 분리:** 환산 정밀도·round-trip → `D-CNV-*` (Decimal/ε). `8.2 feet` 문자열·stderr 전문 → `U-OUT-*` / `U-IN-*` only.

---

## 수행 절차 (Steps)

1. **브랜치 확인** — `green` 브랜치. `refactoring` / `new_features` **생성 금지**.
2. **Target 확정** — 사용자 지정 Test ID. 미지정 시 해당 Track **다음 RED ID**.
3. **Phase 선언** — 필수 선언 형식 출력.
4. **RED 재확인** — Target pytest **FAIL** 실행·로그 기록.
5. **최소 구현** — Target을 통과하는 **가장 작은 diff**만 `src/`에 작성.
   - **NFR-01:** `if unit == "feet"` / 비율 literal 하드코딩 **금지** — `UnitRegistry` SSOT.
   - **entity:** boundary/control/data import **금지**.
   - **에러 문구:** PRD §3.5 전문 equality (`{token}`/`{unit}`/`{value}`/`{reason}` 치환).
6. **테스트 GREEN** — `pytest.fail` 제거, PRD·AC에 맞는 assert 추가.
7. **PASS 확인** — Target 파일(또는 함수) 단일 pytest **PASSED**.
8. **보고** — 아래 형식. **REFACTOR·Golden Master는 별도 Command.**

---

## Domain 예시 (D-CNV-01)

**RED:** `ModuleNotFoundError` 또는 `pytest.fail`

**GREEN 최소:**
- `src/entity/unit_registry.py` — `register`, `get_meters_per_unit`
- `src/entity/conversion_service.py` — `to_meters`: `v_m = v_src * meters_per_unit[src]`
- `tests/`: `pytest.fail` → `assert abs(float(result) - 0.3048) < 1e-9`

```bash
python -m pytest tests/domain/test_d_cnv_01.py -v
```

---

## Boundary 예시 (U-OUT-01)

**GREEN 최소:**
- `src/boundary/cli_parser.py`, `input_validator.py`, `output_formatter.py`, `cli_app.py`
- `src/control/convert_use_case.py`
- RG-04 half-up 1자리 · POLICY-O01 prefix
- AC-01 snapshot: feet `8.2`, yard `2.7`

```bash
python -m pytest tests/boundary/test_u_out_01.py -v
```

---

## pytest 예시 (PowerShell)

```powershell
# Domain — 단일 Target
python -m pytest tests/domain/test_d_cnv_01.py -v

# Boundary — 단일 Target
python -m pytest tests/boundary/test_u_in_01.py -v

# GREEN 게이트 (Must + Should core — EXT 제외)
python -m pytest tests/domain/ tests/boundary/test_u_in_01.py tests/boundary/test_u_in_02.py tests/boundary/test_u_in_03.py tests/boundary/test_u_out_01.py -v
```

---

## GREEN 완료 보고

```markdown
## GREEN Minimal 완료

- Target: D-CNV-01
- RED: FAILED — ModuleNotFoundError: …
- GREEN: PASSED
- 변경: src/entity/*.py, tests/domain/test_d_cnv_01.py
- Mock: Domain Track — 없음
- 다음: 다음 RED Target 또는 /golden-master (Boundary stdout)
```

---

## 성공 조건

- [ ] Target 테스트 **1건** PASS
- [ ] `pytest.fail` / import 실패 **해소**
- [ ] assert **완화·skip·xfail 없음**
- [ ] OCP — ConversionService 단위 분기·비율 literal **0건** (해당 Target 범위)
- [ ] 스펙 없는 알고리즘 invent **없음**
- [ ] REFACTOR·EXT Target **미선행**

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **한 턴에 여러 Target GREEN** | 최소 단위 TDD |
| **assert 완화·skip·xfail** | merge gate 위반 |
| **REFACTOR 선행** | GREEN → REFACTOR 순서 |
| **U-IN + U-OUT 동시 대량 구현** (명시 없을 때) | 범위 초과 |
| **new_features (EXT) 선행** | Phase 분리 |
| **git commit** | 사용자 요청 시만 |
