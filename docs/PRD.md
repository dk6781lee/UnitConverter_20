# UnitConverter_20 — Product Requirements Document (PRD)

| 항목 | 값 |
|------|-----|
| **Version** | 1.0.0-spec |
| **Status** | SSOT — spec 브랜치 |
| **Runtime** | Python 3.11+ |
| **Test** | pytest |
| **Architecture** | BCE (Boundary · Control · Entity) · Dual-Track TDD |
| **References** | `UnitConverter.py`, `README.md`, `Report/01.LegacyAnalysis_Report.md`, `Report/02.SpecPhase_Report.md` |
| **Out of scope** | 본 문서는 **계약·설계 SSOT** — 구현 코드 없음 |

---

## 1. 개요

### 1.1 What

Python CLI 길이 단위 변환기. 사용자가 `{unit}:{value}` 한 줄을 입력하면, **Registry에 등록된 모든 단위**로 변환 결과를 출력한다. 변환은 **meter 허브** 기준으로 수행하며, README 고정 비율을 SSOT로 따른다.

### 1.2 Who

| 역할 | 목적 |
|------|------|
| **실습 참가자** | 레거시(`UnitConverter.py`)를 계약 기반·테스트 가능 구조로 개선 |
| **강사·리뷰어** | FR/NFR/EXT·Test ID·snapshot으로 **객관적 pass/fail** |
| **AI Agent (Cursor)** | RED→GREEN→REFACTOR 시 PRD 문장만으로 판단 |

### 1.3 Why — 계약 · Dual-Track TDD 학습

| 레거시 gap (Report/01) | PRD가 고정하는 것 | 학습 목표 |
|------------------------|-------------------|-----------|
| README 8.2 ft vs 실행 8.2021 | **RG-04** 표시 계약 | Domain 정밀도 ≠ Boundary 표시 |
| `meter:-1` 변환 출력 | **FR-04 / E004** | 검증은 주관적 실행이 아닌 **테스트** |
| if/elif·비율 4곳 중복 | **NFR-01** Registry SSOT | OCP — **ConversionService diff 0** |
| main() 만능 함수 | **NFR-02** BCE 분리 | SRP — Track별 테스트 |
| 테스트·설정·포맷 없음 | **Dual-Track** + EXT | 계약 먼저, 알고리즘 invent 금지 |

**Dual-Track 정의**

- **Domain Track (`D-*`):** `Quantity`, `UnitRegistry`, `ConversionService` — I/O·포맷·에러 문구 **금지**.
- **Boundary Track (`U-*`):** 파싱·stderr/stdout·Formatter — Domain **Mock 허용**, 입출력 문자열·exit code **SSOT**.

**Non-goal:** 환산 알고리즘 연구, GUI, 네트워크, 면적/부피 단위.

---

## 2. 사용자 · 시나리오

### 2.1 Primary Persona

CLI 사용자 — 길이 값을 meter/feet/yard(및 등록 단위)로 동시에 확인.

### 2.2 핵심 시나리오

| # | 시나리오 | 입력 | 기대 |
|---|----------|------|------|
| S-01 | 기본 변환 | `meter:2.5` | stdout 3줄, RG-04, POLICY-O01 |
| S-02 | feet 입력 | `feet:10` | 모든 줄 `10 feet =` 시작 |
| S-03 | zero 허용 | `meter:0` | exit 0, `0 meter = 0.0 …` |
| S-04 | 형식 오류 | `meter` | stderr E001, exit 1 |
| S-05 | 숫자 오류 | `meter:2.5.3` | stderr E002, exit 2 |
| S-06 | 미등록 단위 | `cubit:1` (등록 전) | stderr E003, exit 3 |
| S-07 | 음수 거부 | `meter:-1` | stderr E004, exit 4 |
| S-08 | 설정 로드 | `--config config/units.json` | Registry hydrate, fail-fast |
| S-09 | 동적 등록 | `register 1 cubit = 0.4572 meter` 후 `cubit:1` | EXT-02 |
| S-10 | JSON 출력 | `meter:2.5 --format json` | EXT-03, domain 동형 |

### 2.3 CLI I/O 계약 (Python SSOT)

| 채널 | 용도 |
|------|------|
| **stdin** | 대화형: prompt 후 한 줄 (`UnitConverter.py` 호환 prompt 문구 유지 가능) |
| **stdout** | 성공 시 **변환 결과만** (TEXT/JSON/CSV/table) |
| **stderr** | **모든** `E001`~`E008` 사용자 메시지 |
| **exit code** | `0` = 성공; `1`~`8` = `E001`~`E008` 순서 대응 (아래 §3.4) |

**레거시와의 차이 (의도적):** 레거시는 오류도 `print`→stdout, exit code 미정. 본 PRD는 **stderr + `sys.exit(n)`** 로 단순화·고정.

---

## 3. 기능 요구사항

### 3.1 비즈니스 상수 (README SSOT)

| 관계 | 값 |
|------|-----|
| 1 meter | 3.28084 feet |
| 1 meter | 1.09361 yard |
| feet ↔ yard | **meter 경유만** — 직접 상수 금지 |

**Registry `meters_per_unit` (내부 SSOT)**

| unit | meters_per_unit (Decimal) |
|------|---------------------------|
| meter | `1` |
| feet | `1 / 3.28084` → config `"0.3048"` (4자리 저장, 계산은 Decimal full) |
| yard | `1 / 1.09361` → config `"0.9144"` (4자리 저장, 계산은 Decimal full) |

### 3.2 FR — Functional Requirements

#### FR-01 · 유효 입력 파싱

| 항목 | 계약 |
|------|------|
| **입력** | `{unit}:{value}` — **첫 번째** `:` 기준 분리 (`split(':', 1)`) |
| **trim** | `unit`·`value` 앞뒤 공백 제거 |
| **성공 예** | `meter:2.5` → unit=`meter`, value=`2.5` |
| **거부** | 빈 unit, 빈 value → **E001** |
| **Test** | `U-IN-01` |

#### FR-02 · 전 등록 단위 변환 출력

| 항목 | 계약 |
|------|------|
| **출력 대상** | Registry `list_units()` 순서대로 **모든** 단위 1줄씩 |
| **기본 순서** | `meter`, `feet`, `yard` (bootstrap) |
| **POLICY-O01** | 각 줄은 `{원본값} {원본단위} = {표시값} {대상단위}` 로 **시작** |
| **RG-04** | 표시값 = Domain full precision → **소수 1자리, half-up** |
| **입력 단위 자기 줄** | **포함** (레거시 동작 유지, README `…` 보완) |
| **성공 snapshot** | §7 AC-01 |
| **Test** | `D-CNV-01`, `U-OUT-01` |

#### FR-03 · 미등록 단위 오류

| 항목 | 계약 |
|------|------|
| **입력 예** | `cubit:1` (Registry에 cubit 없음) |
| **stderr** | `E003` SSOT (§3.4) |
| **stdout** | 변환 줄 **0** |
| **exit** | `3` |
| **Test** | `U-IN-03a`, `D-CNV-03c` |

#### FR-04 · 음수 value 거부

| 항목 | 계약 |
|------|------|
| **POLICY-N01** | `numeric_value < 0` → 변환 **금지** |
| **1차 enforcement** | Boundary `InputValidator` (UseCase 호출 전) |
| **2차 invariant** | Domain `Quantity.create` 동일 거부 |
| **입력 예** | `meter:-1` |
| **stderr** | `E004` SSOT |
| **stdout** | **0** 줄 |
| **exit** | `4` |
| **Test** | `U-IN-03b`, `D-CNV-03` |

#### FR-05 · 형식 · 숫자 오류

| 조건 | stderr | exit | 예 |
|------|--------|------|-----|
| `:` 없음 | **E001** | 1 | `meter`, `abc` |
| 숫자 parse 실패 | **E002** | 2 | `meter:abc`, `meter:2.5.3` |
| **Test** | `U-IN-02a/b/c` | | |

**파싱 규칙:** value는 **단일** 유한 Decimal 문자열; `2.5.3`, `1e999` overflow 등 PRD fixture는 **E002**.

#### FR-01 부가 · zero

| 항목 | 계약 |
|------|------|
| **입력** | `meter:0` |
| **exit** | `0` |
| **출력** | `0 meter = 0.0 feet` 등 (RG-04) |
| **Test** | `U-IN-03c`, `D-CNV-03b` |

### 3.3 NFR — Non-Functional Requirements

#### NFR-01 · OCP (측정 가능)

| 항목 | 계약 |
|------|------|
| **정의** | 신규 단위(inch, cubit 등) 추가 시 **`ConversionService`·`Quantity`·`ConvertUseCase` 소스 diff = 0 lines** |
| **허용 변경** | `UnitRegistry`, `IUnitRatioSource`, `config/units.json`, `RegisterUnitUseCase`, Formatter schema, tests |
| **금지** | Converter 내부 `if unit == "feet"` 분기, 비율 literal 하드코딩 |
| **Test** | `D-REG-01`, `D-CFG-01` |

#### NFR-02 · SRP + BCE

| Component | Layer | 단일 책임 |
|-----------|-------|-----------|
| `CliParser`, `InputValidator` | Boundary | 입력 문자열 → DTO / 계약 검증 |
| `OutputFormatter`, `ErrorPresenter` | Boundary | Domain 결과 → stdout / E00x → stderr |
| `ConvertUseCase`, `RegisterUnitUseCase`, `LoadConfigUseCase` | Control | 오케스트레이션 |
| `Quantity`, `UnitRegistry`, `ConversionService` | Entity | 순수 도메인 |
| `JsonUnitRatioSource` | Data (Boundary-adjacent) | 설정 로드 |

### 3.4 EXT — Extensions

#### EXT-01 · 설정 외부화

| 항목 | 계약 |
|------|------|
| **파일** | `config/units.json` (기본 경로; CLI `--config` 로 override) |
| **성공** | Registry bootstrap |
| **실패** | **E005**, exit 5, **default 3단위 fallback 금지** |
| **Test** | `D-CFG-01` |

#### EXT-02 · 동적 단위 등록

| 항목 | 계약 |
|------|------|
| **등록 문법** | `register 1 {name} = {ratio} meter` (§5.2) |
| **성공** | 동일 프로세스 Registry에 반영 |
| **실패** | **E006**, exit 6 |
| **Test** | `D-REG-01` + AC-05 |

#### EXT-03 · 출력 포맷

| `--format` | stdout |
|------------|--------|
| `text` (default) | POLICY-O01 + RG-04 줄 목록 |
| `json` | §6.2 JSON schema |
| `csv` | §6.3 CSV |
| `table` | §6.4 table |
| 잘못된 값 | **E007**, exit 7 |

**Domain 동형성:** 동일 입력·Registry → 포맷만 다름; **환산값 집합 동일** (`U-OUT-01b/c/d`).

### 3.5 에러 코드 SSOT (E001~E008)

Python `print(msg, file=sys.stderr)` + `sys.exit(code)`.

| Code | exit | stderr 메시지 (전문 equality — `{…}` 치환) | FR/EXT |
|------|------|---------------------------------------------|--------|
| **E001** | 1 | `Invalid format. Use unit:value (ex: meter:2.5)` | FR-05 |
| **E002** | 2 | `Invalid number: {token}` | FR-05 |
| **E003** | 3 | `Unknown unit: {unit}` | FR-03 |
| **E004** | 4 | `Negative value not allowed: {value}` | FR-04 |
| **E005** | 5 | `Config load failed: {reason}` | EXT-01 |
| **E006** | 6 | `Invalid unit registration: {reason}` | EXT-02 |
| **E007** | 7 | `Invalid output format: {format}` | EXT-03 |
| **E008** | 8 | `Internal error: {code}` | Domain bug — Domain TC 0건 목표 |

**레거시 채택:** E001~E003 문구는 `UnitConverter.py` L5/L13/L23과 **호환**. E004~E008은 Python stderr/exit 정책에 맞게 **신규 SSOT**.

---

## 4. 비기능 · 아키텍처 · 품질

### 4.1 BCE + Dual-Track

```
Boundary: CliParser → InputValidator → ErrorPresenter
              ↓
Control:    ConvertUseCase | RegisterUnitUseCase | LoadConfigUseCase
              ↓
Entity:     Quantity → ConversionService ← UnitRegistry
              ↑
Data:       JsonUnitRatioSource (IUnitRatioSource)
              ↓
Boundary:   OutputFormatter → stdout
```

### 4.2 Dual-Track 테스트 규칙

| Track | Suite | Mock | Assert |
|-------|-------|------|--------|
| Domain | `tests/domain/` | 금지 | Decimal, DomainError |
| Boundary | `tests/contract/` | Service/Registry 허용 | stderr, stdout, exit |
| Data | `tests/data/` | temp files | LoadError→E005 |

**중복 금지:** 환산식 정확도 → `D-CNV-*` only. `8.2 feet` 문자열 → `U-OUT-*` only.

### 4.3 커버리지 목표 (팀 합의 — 변경 시 본 절 PR만 수정)

| 범위 | 목표 | 측정 |
|------|------|------|
| Entity (`src/domain/`) | **line 100%** | pytest-cov |
| Boundary contract | **FR/EXT stderr·stdout 경로 100%** | Test ID C2C 표 전건 |
| Control | **UseCase happy + error map 100%** | integration |
| **Overall** | **≥ 90%** | `pytest --cov=src` |
| **Skip/xfail** | **0** (RED Phase 예외: red 브랜치만, merge 전 0) | CI gate |

---

## 5. 데이터

### 5.1 `config/units.json` schema

```json
{
  "$schema": "unitconverter/units-v1",
  "units": [
    { "name": "meter", "meters_per_unit": "1" },
    { "name": "feet",  "meters_per_unit": "0.3048" },
    { "name": "yard",  "meters_per_unit": "0.9144" }
  ]
}
```

| Field | Type | Rule |
|-------|------|------|
| `units` | array | ≥1 |
| `name` | string | `[a-z][a-z0-9_]*`, duplicate → E005 |
| `meters_per_unit` | string (Decimal) | **> 0**; 0 or negative → E005 |

**YAML:** v1 optional; JSON SSOT 우선.

### 5.2 동적 등록 형식 (EXT-02)

**입력 줄 (stdin 또는 subcommand):**

```text
register 1 cubit = 0.4572 meter
```

| Token | Rule |
|-------|------|
| `register` | literal |
| `1` | optional coefficient (default 1) |
| `{name}` | unit name, schema 동일 |
| `{ratio}` | Decimal > 0 |
| `meter` | hub literal (v1) |

**의미:** `meters_per_unit(cubit) = ratio / coefficient` → example: `0.4572`.

**성공 응답 (stdout):** `Registered unit: cubit`

---

## 6. 출력

### 6.1 TEXT (default) — RG-04

**AC-01 snapshot (`meter:2.5`):**

```text
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard
```

| Rule | ID |
|------|-----|
| 소수 1자리 half-up | RG-04 |
| 모든 줄 원 입력 prefix | POLICY-O01 |

### 6.2 JSON (`--format json`)

```json
{
  "source": { "unit": "meter", "value": "2.5" },
  "conversions": [
    { "unit": "meter", "value": "2.5", "display": "2.5" },
    { "unit": "feet",  "value": "8.2021", "display": "8.2" },
    { "unit": "yard",  "value": "2.734025", "display": "2.7" }
  ]
}
```

- `value`: Domain full precision string (Decimal)
- `display`: RG-04

### 6.3 CSV (`--format csv`)

```text
source_unit,source_value,target_unit,target_display
meter,2.5,meter,2.5
meter,2.5,feet,8.2
meter,2.5,yard,2.7
```

RFC4180 escaping. Header row **필수**.

### 6.4 table (`--format table`)

```text
| meter | 2.5 | feet | 8.2 |
| meter | 2.5 | yard | 2.7 |
| meter | 2.5 | meter | 2.5 |
```

Columns: `source_unit | source_value | target_unit | target_display`. Row order = Registry order.

---

## 7. 인수 조건 (Acceptance Criteria)

| AC ID | 조건 | Verify |
|-------|------|--------|
| **AC-01** | `meter:2.5` TEXT = §6.1 snapshot **exact** | `U-OUT-01` snapshot |
| **AC-02** | `feet:10` 모든 TEXT 줄 `10 feet =` prefix | POLICY-O01 |
| **AC-03** | `meter:0` exit 0; `0 meter = 0.0 feet`, `0 meter = 0.0 yard` | `U-IN-03c` |
| **AC-04** | `meter` → E001 exit 1; `meter:2.5.3` → E002 exit 2; `meter:-1` → E004 exit 4 | `U-IN-02`, `U-IN-03b` |
| **AC-05** | `register 1 cubit = 0.4572 meter` 후 `cubit:1` exit 0, cubit 줄 포함 | EXT-02 integration |
| **AC-06** | `config/units.json` + inch → ConversionService **diff 0**, pytest green | NFR-01 gate |
| **AC-07** | missing config → E005, **no** default conversion output | `D-CFG-01b` |
| **AC-08** | `--format json|csv|table` domain 동형 | `U-OUT-01b/c/d` |
| **AC-09** | `pytest tests/` 전건 green, skip/xfail 0 | CI |
| **AC-10** | FR-01~05, NFR-01~02, EXT-01~03 C2C 표 **누락 0** | §10 checklist |

---

## 8. 회귀 (RG)

### 8.1 RG-04 · 표시 회귀

| ID | Guard |
|----|-------|
| **RG-04** | TEXT/CSV/table `display` — **1 decimal half-up**; 변경 시 **AC-01 snapshot** 동시 갱신 |

### 8.2 Domain / Boundary TC

| Suite | Merge gate |
|-------|------------|
| `tests/domain/test_d_*.py` | **전건 GREEN** |
| `tests/contract/test_u_*.py` | **전건 GREEN** |
| `tests/data/test_d_cfg_*.py` | **전건 GREEN** |

### 8.3 Snapshot 변경 절차

1. PRD §6/§7 또는 본 RG 섹션 **먼저** 수정 (팀 리뷰)
2. `tests/fixtures/snapshots/` 갱신
3. PR 본문: **변경 이유** + Report/01 레거시 diff 참조
4. `RG-04` 또는 `POLICY-O01` 변경은 **강사 승인** 필수

**금지:** snapshot만 바꾸고 PRD 미갱신.

---

## 9. Glossary

| Term | Definition |
|------|------------|
| **BCE** | Boundary · Control · Entity 레이어 |
| **Dual-Track** | Domain 테스트(`D-*`) vs Boundary 계약 테스트(`U-*`) 분리 |
| **meter 허브** | 모든 환산의 중간 기준 단위 |
| **meters_per_unit** | 1 `{unit}` = `{ratio}` meter |
| **Registry SSOT** | 단위명·비율의 유일한 진실 원 |
| **POLICY-O01** | 출력 줄 prefix = 원본 `{value} {unit} =` |
| **POLICY-N01** | 음수 value 거부; E004 |
| **RG-04** | 표시 소수 1자리 half-up |
| **Domain full precision** | Formatter 이전 Decimal — 테스트는 epsilon 또는 exact Decimal |
| **ConversionService** | Entity 환산 — **OCP core** (diff 0 대상) |
| **Fail-fast** | config 실패 시 bootstrap fallback 금지 |
| **C2C** | Concept → Requirement → Test ID → Component 추적 |
| **RED/GREEN** | TDD Phase; red 브랜치에서만 의도적 fail 허용 |

---

## 10. Traceability — Test ID C2C

| Test ID | FR/NFR/EXT | Concept | UseCase | Component | Contract Test |
|---------|------------|---------|---------|-----------|---------------|
| **D-CNV-01** | FR-02 | hub conversion | ConvertUseCase | ConversionService | `meter:2.5` internal feet/yard |
| **D-CNV-02** | FR-02 | round-trip | ConvertUseCase | ConversionService | feet→meter→feet |
| **D-CNV-03** | FR-04 | negative invariant | — | Quantity | `Quantity(-1)` → DomainError |
| **D-CNV-03b** | FR-01 | zero | ConvertUseCase | Quantity, ConversionService | `meter:0` |
| **D-REG-01** | NFR-01, FR-03 | registry SSOT | RegisterUnitUseCase | UnitRegistry | inch add; **core diff 0** |
| **D-REG-01b** | D-INV-02 | factor>0 | RegisterUnitUseCase | UnitRegistry | zero factor reject |
| **D-CFG-01a** | EXT-01 | config load | LoadConfigUseCase | JsonUnitRatioSource | valid + inch |
| **D-CFG-01b** | EXT-01 | fail-fast | LoadConfigUseCase | JsonUnitRatioSource | missing → E005 |
| **D-CFG-01c** | EXT-01 | invalid schema | LoadConfigUseCase | JsonUnitRatioSource | factor 0 → E005 |
| **U-IN-01** | FR-01 | valid parse | ConvertUseCase | CliParser | `meter:2.5` |
| **U-IN-02a** | FR-05 | format | — | InputValidator | `meter` → E001 |
| **U-IN-02b** | FR-05 | decimal fail | — | InputValidator | `meter:2.5.3` → E002 |
| **U-IN-02c** | FR-05 | alpha num | — | InputValidator | `meter:abc` → E002 |
| **U-IN-03a** | FR-03 | unknown | ConvertUseCase | InputValidator | `cubit:1` → E003 |
| **U-IN-03b** | FR-04 | negative | — | InputValidator | `meter:-1` → E004 |
| **U-IN-03c** | FR-01 | zero | ConvertUseCase | InputValidator | `meter:0` ok |
| **U-OUT-01** | FR-02, RG-04, POLICY-O01 | TEXT snapshot | ConvertUseCase | OutputFormatter | AC-01, AC-02 |
| **U-OUT-01b** | EXT-03 | JSON | ConvertUseCase | OutputFormatter | schema |
| **U-OUT-01c** | EXT-03 | CSV | ConvertUseCase | OutputFormatter | header+rows |
| **U-OUT-01d** | EXT-03 | table | ConvertUseCase | OutputFormatter | snapshot |
| **U-OUT-02** | EXT-03 | bad format | ConvertUseCase | CliApp | `--format xml` → E007 |

### 10.1 C2C 완료 체크리스트

- [ ] FR-01~05 각 ≥1 Test ID
- [ ] NFR-01: `D-REG-01` + **ConversionService diff 0** 명시
- [ ] NFR-02: Component表 §3.3 매핑
- [ ] EXT-01~03: `D-CFG-*`, `U-OUT-01b/c/d`, EXT-02 AC-05
- [ ] E001~E008: exit code · stderr 전문 §3.5
- [ ] AC-01~AC-10 전건 Test ID 연결

---

## 11. Git · Phase (참조)

| 브랜치 | Phase | 산출물 |
|--------|-------|--------|
| `staging` | 명세 시작 | Report/01 |
| **`spec`** | **PRD SSOT** | **본 문서** |
| `red` | RED tests | failing pytest |
| `green` | minimal pass | |
| `refactoring` | BCE split | |
| `new_features` | EXT | |

merge · branch 삭제 · spec 이후 브랜치 선행 생성 **금지** (Report/01 §8).

---

## 12. Document History

| Version | Date | Change |
|---------|------|--------|
| 1.0.0-spec | 2026-06-05 | Initial SSOT — Report/01 레거시·README·Dual-Track 설계 반영 |

---

*docs/PRD.md · UnitConverter_20 · spec · 구현 없음 · pytest Test ID SSOT*
