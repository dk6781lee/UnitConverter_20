---
description: TDD RED 설계표만 — C2C·Given/Then 표, tests/src 파일 생성 금지
---

# RED Test Plan — 설계표만

UnitConverter_20 **RED Phase 설계** — **표·계획만** 출력한다.  
**근거:** `.cursorrules` · `docs/PRD.md` §10 (Test ID C2C)

**다음 단계:** `/red-skeleton` — 스켈레톤 작성 + pytest FAIL 확인

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: red | Layer: entity|control|boundary|data | Track: Domain|Boundary|Data | Target: D-*|U-*
```

---

## 목적 (Objective)

- `docs/PRD.md` §10에서 **Target Test ID** 1건(또는 사용자 지정 묶음)의 **RED 설계표**를 작성한다.
- **파일을 만들지 않는다** — `tests/`, `src/`, `config/` 미수정.
- **pytest를 실행하지 않는다**.
- GREEN·REFACTOR·skeleton 구현은 **하지 않는다**.

---

## Track · Layer · 파일 매핑 (계획용)

| Track | Layer | pytest 파일 (계획) | Test ID | Mock |
|-------|-------|-------------------|---------|------|
| **Domain** | entity, control | `tests/domain/test_d_*.py` | `D-*` | Domain Mock **금지** |
| **Boundary** | boundary | `tests/boundary/test_u_*.py` | `U-*` | `ConvertUseCase` 등 Mock **허용** |
| **Data** | data | `tests/data/test_d_cfg_*.py` | `D-CFG-*` | temp config files only |

**Assert 분리:** 환산 정밀도 → `D-CNV-*`. `8.2 feet` 문자열 → `U-OUT-*` only.

---

## 수행 절차 (Steps)

1. **Target 확정** — `docs/PRD.md` §10 C2C 표에서 Test ID 선택.
2. **Phase 선언** — 필수 선언 형식 출력.
3. **설계표 작성** — 아래 **보고 형식** 표만 출력 (추가 prose 최소화).
4. **Harness 확인** — `pyproject.toml`, `tests/{domain,boundary,data}/`, `config/units.json` 존재 여부만 언급 가능.
5. **완료 한 줄** — `/red-skeleton` 준비됐다고 안내.

---

## pytest 예시 (참고 — 본 Phase에서 실행 금지)

```bash
# /red-skeleton 완료 후 실행 (Domain)
python -m pytest tests/domain/test_d_cnv_01.py -v

# Boundary
python -m pytest tests/boundary/test_u_out_01.py -v

# Data
python -m pytest tests/data/test_d_cfg_01a.py -v
```

> **본 커맨드(`red-test-plan`)에서는 위 명령을 실행하지 않는다.**

---

## 보고 형식

### Domain Track (예: D-CNV-01)

| # | 항목 | 내용 |
|---|------|------|
| 1 | **C2C** | FR/NFR → Test ID → UseCase → Component (PRD §10) |
| 2 | **Given / When / Then** | Domain `Decimal`·실객체; Formatter/stdout **미사용** |
| 3 | **BCE · Mock** | Layer · Track Mock 규칙 |
| 4 | **pytest 파일** | `tests/domain/test_d_*.py` · 함수명 예시 |

### Boundary Track (예: U-IN / U-OUT 묶음)

| Test ID | Given | Then | Expected RED Failure |
|---------|-------|------|----------------------|
| **U-IN-01** | … | stderr E001 · exit 1 | `ImportError` / assert FAILED |
| **U-OUT-01** | stdin `meter:2.5` | AC-01 snapshot 문자열 | `ModuleNotFoundError` / assert FAILED |

### Data Track (예: D-CFG-01a)

| # | 항목 | 내용 |
|---|------|------|
| 1 | **C2C** | EXT-01 → `D-CFG-01a` → `JsonUnitRatioSource` |
| 2 | **Given / When / Then** | `config/units.json` 또는 temp file |
| 3 | **Then** | load 성공 / E005 fail-fast |
| 4 | **pytest 파일** | `tests/data/test_d_cfg_01.py` |

---

## Plan 완료 보고

```markdown
## RED Plan 완료

- Target: D-CNV-01
- Track: Domain · Layer: entity
- pytest 파일 (예정): tests/domain/test_d_cnv_01.py
- Mock: 없음 (Domain Track)
- 다음: /red-skeleton — 스켈레톤 작성 + pytest FAIL
```

---

## 성공 조건

- [ ] PRD §10 Test ID와 **C2C 연결** 명시
- [ ] Given / When / Then (또는 Given / Then) **계약 수준** 기술
- [ ] Expected RED Failure 유형 명시 (`ImportError`, `pytest.fail`, assert FAILED)
- [ ] **`tests/` · `src/` · `config/` 파일 생성·수정 없음**
- [ ] **pytest 미실행**

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **`tests/` · `src/` · `UnitConverter.py` 생성·수정** | Plan = 설계만 |
| **pytest 실행** | skeleton Phase 책임 |
| **assert·구현 코드 작성** | skeleton/GREEN 책임 |
| **GREEN / REFACTOR** | RED 순서 |
| **skip / xfail 제안** | merge gate 위반 |
| **git commit** | 사용자 요청 시만 |
