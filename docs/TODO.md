# UnitConverter_20 — TODO

| 항목 | 값 |
|------|-----|
| **SSOT** | `docs/PRD.md` |
| **브랜치** | Must/Should → `green` · `refactoring` · Nice → `new_features` |
| **금지** | skip · xfail · merge · branch 선행 생성 |
| **회귀 명령** | `pytest tests/ -v` |

> 본 문서는 **작업 목록·완료 기준**만 기술 — 구현 코드 없음.

---

## 🔴 Must — FR · NFR · Domain TC (`D-CNV`, `D-REG`)

**목표 브랜치:** `red` (FAIL) → `green` (PASS)  
**Suite:** `tests/domain/test_d_*.py`

| # | 작업 | PRD ID | Test ID | 완료 기준 (테스트 가능) |
|---|------|--------|---------|-------------------------|
| M-01 | README 3단위 Registry bootstrap | FR-02 · NFR-01 | D-REG-01 | `UnitRegistry.list_units()` = `[meter, feet, yard]`; `meters_per_unit` README SSOT |
| M-02 | meter 허브 환산 — meter 입력 | FR-02 | D-CNV-01 | `meter:2.5` → feet=`2.5×3.28084`, yard=`2.5×1.09361` (PRD epsilon 내) |
| M-03 | 전 등록 단위 line 수 | FR-02 | D-CNV-01 | `ConversionResult.lines` count = Registry unit count |
| M-04 | feet↔yard meter 경유 (직접 상수 0) | FR-02 · README | D-CNV-02 | feet→yard = feet→meter→yard; ConversionService 내 feet-yard literal **0건** |
| M-05 | round-trip feet · yard | FR-02 | D-CNV-02 | feet→meter→feet · yard→meter→yard Decimal equality (허용 오차 내) |
| M-06 | Domain 음수 invariant | FR-04 · POLICY-N01 | D-CNV-03 | `Quantity.create(-1)` → DomainError; `convert` 미호출 |
| M-07 | zero meter Domain | FR-01 | D-CNV-03b | `Quantity(0)` → 모든 target internal value = 0 |
| M-08 | 미등록 단위 Domain | FR-03 | D-CNV-03c | unregistered unit → DomainError UNKNOWN_UNIT |
| M-09 | factor > 0 Registry | D-INV-02 · NFR-01 | D-REG-01b | `meters_per_unit ≤ 0` 등록 → reject; Registry unchanged |
| M-10 | inch 등록 OCP gate | NFR-01 | D-REG-01 · NFR-01-OCP | inch 등록 후 **`ConversionService`·`Quantity` git diff = 0**; `D-REG-01` green |
| M-11 | ConversionService 비율 literal 0 | NFR-01 | D-CNV-01 | static review + test: Service 내부 `3.28084`/`1.09361` literal **0건** |
| M-12 | Domain suite merge gate | AC-09 | `tests/domain/` | `pytest tests/domain/ -v` — **failed=0, skipped=0, xfailed=0** |

---

## 🟡 Should — Boundary TC (`U-IN`, `U-OUT`) · REFACTOR

**목표 브랜치:** `green` (Boundary core) → `refactoring` (BCE split)  
**Suite:** `tests/contract/test_u_*.py` · `tests/contract/test_nfr_02_bce.py`

### Boundary — 입력 (`U-IN`)

| # | 작업 | PRD ID | Test ID | 완료 기준 (테스트 가능) |
|---|------|--------|---------|-------------------------|
| S-01 | 유효 파싱 | FR-01 | U-IN-01 | `meter:2.5` → exit 0; ParsedInput `(meter, 2.5)` UseCase 전달 |
| S-02 | 형식 오류 `:` 없음 | FR-05 · E001 | U-IN-02a | `meter` → stderr E001 **전문 equality**, exit=1, stdout 0줄 |
| S-03 | 숫자 오류 `2.5.3` | FR-05 · E002 | U-IN-02b | `meter:2.5.3` → stderr E002, exit=2, stdout 0줄 |
| S-04 | 숫자 오류 `abc` | FR-05 · E002 | U-IN-02c | `meter:abc` → stderr E002, exit=2 |
| S-05 | 빈 unit / 빈 value | FR-05 · E001 | U-IN-02c | `meter:` · `:2.5` → E001 |
| S-06 | 미등록 단위 | FR-03 · E003 | U-IN-03a | `cubit:1` → stderr E003, exit=3, stdout 0줄 |
| S-07 | Boundary 음수 거부 | FR-04 · E004 | U-IN-03b | `meter:-1` → stderr E004, exit=4, stdout 0줄; UseCase **미호출** |
| S-08 | zero 허용 Boundary | FR-01 | U-IN-03c | `meter:0` → exit 0; **not** E004 |

### Boundary — 출력 (`U-OUT`)

| # | 작업 | PRD ID | Test ID | 완료 기준 (테스트 가능) |
|---|------|--------|---------|-------------------------|
| S-09 | AC-01 TEXT snapshot | FR-02 · RG-04 · AC-01 | U-OUT-01 | `meter:2.5` stdout **3줄 전문** = PRD §6.1 |
| S-10 | POLICY-O01 prefix | FR-02 · POLICY-O01 · AC-02 | U-OUT-01 | `feet:10` — **모든** stdout 줄이 `10 feet =` 로 시작 |
| S-11 | stderr/stdout 분리 | §2.3 · E001~E004 | U-IN-02* · U-IN-03* | 오류 메시지 **stderr only**; stdout 변환 줄 0 |
| S-12 | Contract suite gate | AC-09 | `tests/contract/` (EXT 제외) | `pytest tests/contract/test_u_in*.py tests/contract/test_u_out_01.py -v` green |

### REFACTOR — BCE · SRP

| # | 작업 | PRD ID | Test ID | 완료 기준 (테스트 가능) |
|---|------|--------|---------|-------------------------|
| S-13 | Parser 단일 책임 | NFR-02 | NFR-02-BCE | CliParser: parse only — convert/format **import 0** |
| S-14 | InputValidator 단일 책임 | NFR-02 · FR-04/05 | NFR-02-BCE | Validator: 검증 only — Registry mutate **0** |
| S-15 | ConversionService I/O free | NFR-02 | D-CNV-* regression | Domain tests pass with **no** stdin/stdout mock in Entity |
| S-16 | OutputFormatter 계산 free | NFR-02 · RG-04 | U-OUT-01 | Formatter: RG-04·POLICY-O01 only — ratio calc **0** |
| S-17 | ConvertUseCase orchestration | NFR-02 | U-IN-01 · U-OUT-01 | Control: if/elif unit 분기 **0** |
| S-18 | REFACTOR regression | AC-09 · §8.2 | `tests/domain/` + contract core | `pytest tests/ -v` (EXT 제외) green; **ConversionService diff 0** 유지 |

**REFACTOR 브랜치:** `refactoring`

---

## 🟢 Nice — EXT-01~03 (`new_features`)

**목표 브랜치:** `new_features`  
**Suite:** `tests/data/test_d_cfg_01.py` · EXT rows in `test_d_reg_01.py` · `test_u_out_01.py` · `test_u_out_02.py`

| # | 작업 | PRD ID | Test ID | 완료 기준 (테스트 가능) |
|---|------|--------|---------|-------------------------|
| N-01 | units.json valid load | EXT-01 · AC-06 | D-CFG-01a | valid JSON → inch in Registry; `ConversionService` diff 0 |
| N-02 | config missing fail-fast | EXT-01 · AC-07 · E005 | D-CFG-01b | missing file → E005 exit 5; **no** default 3-unit fallback output |
| N-03 | config invalid schema | EXT-01 · E005 | D-CFG-01c | factor=0 · duplicate name → E005; partial Registry **0** |
| N-04 | 동적 cubit 등록 | EXT-02 · AC-05 | D-REG-02 | `register 1 cubit = 0.4572 meter` 후 `cubit:1` exit 0 |
| N-05 | cubit 등록 전 E003 | EXT-02 · FR-03 | D-REG-02 | 등록 전 `cubit:1` → E003; 등록 후 → FR-02 |
| N-06 | invalid register → E006 | EXT-02 · E006 | D-REG-02 | bad syntax · duplicate → E006 exit 6 |
| N-07 | JSON 출력 | EXT-03 · AC-08 | U-OUT-01b | `--format json` parse OK; `display` RG-04; `value` full precision |
| N-08 | CSV 출력 | EXT-03 · AC-08 | U-OUT-01c | header PRD §6.3 equality; rows = unit count |
| N-09 | table 출력 | EXT-03 · AC-08 | U-OUT-01d | 4-column snapshot; row order = Registry order |
| N-10 | invalid format → E007 | EXT-03 · E007 | U-OUT-02 | `--format xml` → E007 exit 7; stdout 0 |
| N-11 | 포맷 동형성 | EXT-03 · AC-08 | U-OUT-01b/c/d | json/csv/table canonical value set **identical** |
| N-12 | Full EXT gate | AC-09 · AC-10 | `tests/` | `pytest tests/ -v` — **전 suite green**, skip/xfail 0 |

---

## 🔵 Tech Debt — 레거시 · 구조 부채

| # | 작업 | PRD ID | 근거 | 완료 기준 (테스트 가능) |
|---|------|--------|------|-------------------------|
| T-01 | `UnitConverter.py` if/elif unit 분기 제거 | NFR-01 · Report/01 §3 | L16~24 | `grep`/`rg` `elif unit` in `src/` = **0**; D-REG-01 green |
| T-02 | 비율 literal 4곳 중복 제거 | NFR-01 · EXT-01 | L19~28 | `3.28084`/`1.09361` in `src/` = Registry/config **only** |
| T-03 | main() SRP 분해 | NFR-02 | L1~32 | `UnitConverter.py` deprecated or thin entry; logic in BCE modules |
| T-04 | 오류 stdout → stderr 마이그레이션 | §2.3 · E001~E004 | 레거시 L5/L13/L23 | U-IN-02/03 contract green; stdout에 E00x **0건** |
| T-05 | exit code 도입 | §2.3 | 레거시 implicit 0 | E001~E007 exit 1~7 contract tests green |
| T-06 | float → Decimal (Domain) | FR-02 · D-INV-01 | 레거시 float | D-CNV-01/02 epsilon tests green without float drift |
| T-07 | 레거시 표시 drift 제거 | RG-04 · AC-01 | 8.2021 vs 8.2 | U-OUT-01 snapshot = PRD §6.1 exactly |
| T-08 | 음수 허용 제거 | FR-04 | Report/01 §4 | `meter:-1` manual run + U-IN-03b + D-CNV-03 green |
| T-09 | Domain/Boundary 중복 assert 정리 | Dual-Track · §4.2 | C2C | 환산식 → D-CNV only; snapshot/E00x → U-* only |
| T-10 | 레거시 파일 역할 문서화 | — | README 실행 경로 | README 또는 PRD에 new entrypoint 경로 명시; AC-09 green |

---

## 📋 회귀 (Regression)

### 매 merge / Phase 전환 전 필수

| # | 절차 | PRD ID | 완료 기준 (테스트 가능) |
|---|------|--------|-------------------------|
| R-01 | Full verbose run | AC-09 · §8.2 | `pytest tests/ -v` → **failed=0, skipped=0, xfailed=0** |
| R-02 | Domain track | §8.2 | `pytest tests/domain/ -v` → 전건 green |
| R-03 | Boundary track | §8.2 | `pytest tests/contract/ -v` → 전건 green |
| R-04 | Data track | §8.2 | `pytest tests/data/ -v` → 전건 green (EXT Phase 이후) |
| R-05 | **meter:2.5 snapshot** | AC-01 · RG-04 · U-OUT-01 | stdout 3줄 = PRD §6.1 **byte-identical** (line endings SSOT) |
| R-06 | feet:10 prefix | AC-02 · POLICY-O01 | 모든 줄 `10 feet =` 시작 |
| R-07 | 에러 4종 smoke | FR-03~05 · FR-04 | `meter`→E001 · `meter:2.5.3`→E002 · `cubit:1`→E003 · `meter:-1`→E004 |
| R-08 | OCP gate | NFR-01-OCP · AC-06 | inch/cubit 추가 PR에서 ConversionService diff **0** |
| R-09 | Snapshot 변경 절차 | §8.3 | PRD §6/§7 **선행 수정** + 강사 승인(RG-04/POLICY-O01) + snapshot commit |
| R-10 | Coverage (팀 합의) | §4.3 | `pytest --cov=src` ≥ **90%**; Entity **100%** |

### PRD §6.1 snapshot (회귀 SSOT)

```text
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

---

## Phase · 브랜치 체크리스트

| Phase | Branch | TODO 섹션 | Gate |
|-------|--------|-----------|------|
| RED | `red` | Must tests exist, **intentional FAIL** | failed ≥ 25, skipped=0 |
| GREEN | `green` | 🔴 Must + 🟡 U-IN/U-OUT core | R-01~R-07 green |
| REFACTOR | `refactoring` | 🟡 REFACTOR + 🔵 T-01~T-06 | S-13~S-18 · NFR-01-OCP |
| EXT | `new_features` | 🟢 Nice | N-01~N-12 · R-04 |
| Done | — | 📋 R-01~R-10 | AC-01~AC-10 |

---

## 진행 상태 (수동 갱신)

| 섹션 | 항목 수 | Done | Blocker |
|------|---------|------|---------|
| 🔴 Must | 12 | 0 | `red` 브랜치 미생성 |
| 🟡 Should | 18 | 0 | Domain Must 선행 |
| 🟢 Nice | 12 | 0 | `new_features` Phase |
| 🔵 Tech Debt | 10 | 0 | REFACTOR Phase |
| 📋 회귀 | 10 | — | 매 Phase gate |

---

*docs/TODO.md · spec · PRD v1.0.0-spec · 코드 없음 · 최종 갱신 2026-06-05*
