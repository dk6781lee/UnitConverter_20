---
description: BCE·Dual-Track read-only 리뷰 — import/OCP/SRP/Mock 위반 표, 코드 수정 금지
---

# BCE · Dual-Track Review — read-only

UnitConverter_20 **아키텍처·계약 준수 리뷰만** 수행한다.  
**근거:** `.cursorrules` · `docs/PRD.md` §3~§4 · §10

**코드·테스트·설정 파일 수정 금지.** 위반만 표로 보고한다.

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: review | Scope: src/|tests/|all | Track: Domain|Boundary|Data|all
```

---

## 목적 (Objective)

- BCE **import 방향**, **OCP/SRP**, **Dual-Track Mock**, **계약(SSOT)** 위반을 탐지한다.
- 수정 제안은 **텍스트**로만. 자동 fix·리팩터·commit **하지 않는다**.

---

## 점검 절차 (Steps)

1. **범위 확인** — 사용자 지정 또는 `git diff` / 최근 변경 파일.
2. **정적 스캔** — Read·Grep으로 아래 체크리스트 검사.
3. **위반 표** — 발견 항목만 행으로 기록. 없으면 `위반 없음`.
4. **요약** — P0(merge blocker) / P1(nit) 구분.

---

## 체크리스트

### 1. BCE import 방향

| 허용 | 금지 |
|------|------|
| `boundary → control` | `entity → boundary` / `control` / `data` |
| `control → entity` | `boundary → entity` (직접) |
| `data → entity` (port) | `entity`에서 I/O·상위 레이어 import |

**Grep 힌트:** `from (boundary|control|data)`, `import sys` in `src/entity/`

### 2. OCP · SRP

| 항목 | 위반 신호 |
|------|-----------|
| **OCP** | `if unit == "feet"` / elif 단위 체인; 비율 literal 중복 |
| **OCP** | 단위 추가 시 `ConversionService` **diff ≠ 0** |
| **SRP** | Parser·Registry·Converter·Formatter·main() 한 파일/클래스 혼재 |
| **SSOT** | `config/units.json` 외 비율 하드코딩 |

### 3. Dual-Track Mock

| Track | 규칙 | 위반 |
|-------|------|------|
| **Domain** `tests/domain/` | 실객체 only | `@patch`, `MagicMock` on Registry·ConversionService |
| **Boundary** `tests/boundary/` | Mock 허용 | entity 직접 import로 CLI 우회 |
| **Data** `tests/data/` | temp config files | production `config/units.json` 변조 |

### 4. Assert · Track 중복

| 항목 | 규칙 |
|------|------|
| Domain 정밀도 | `D-CNV-*` — Decimal / ε (예: 8.20210 ft) |
| Boundary 표시 | `U-OUT-*` — RG-04 문자열 (예: 8.2 feet) |
| 혼용 | Domain 테스트에 `8.2` snapshot assert → **P0** |

### 5. 계약 · TDD

| 항목 | SSOT |
|------|------|
| stderr/exit | E001~E008 전문·exit code (`docs/PRD.md` §3.5) |
| TDD 순서 | RED FAIL 선행 없이 `src/` 구현 |
| 우회 | assert 완화, `skip`, `xfail`, RED 테스트 삭제 |

---

## 리뷰 보고 형식

```markdown
## BCE Review

| P | Track | File | Rule | Finding |
|---|-------|------|------|---------|
| P0 | Domain | tests/domain/… | Mock 금지 | @patch ConversionService |
| P1 | — | — | — | (없으면 위반 없음) |

- P0: N건 · P1: N건
- 권장: (수정은 사용자/별도 Phase에서)
```

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **파일 Write/Edit** | read-only 리뷰 |
| **자동 fix·리팩터** | 판정과 구현 분리 |
| **git commit / push** | 사용자 요청 시만 |
| **스펙 없는 신규 요구 제안** | PRD SSOT |
