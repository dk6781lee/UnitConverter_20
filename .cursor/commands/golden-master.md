---
description: Golden Master — Boundary stdout/stderr 승인 스냅샷 고정, src/ 로직 변경 금지
---

# Golden Master — 승인 출력 회귀 고정

UnitConverter_20 **Boundary Track** — **stdout/stderr 전문**을 golden 파일로 고정한다.  
**근거:** `.cursorrules` · `docs/PRD.md` §6.1 (AC-01) · RG-04 · POLICY-O01  
**선행:** `/green-minimal` 완료 — Target Boundary 테스트 **이미 PASS** (GRN-P3)

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: green | Layer: boundary | Track: Boundary | Golden: U-OUT-*|U-IN-*
```

---

## 목적 (Objective)

- **프로덕션 로직(`src/`)은 변경하지 않고** `tests/`만 수정한다.
- Boundary **stdout/stderr 전문**을 `tests/golden/*.approved.txt`에 저장한다.
- 이후 회귀 시 실제 출력과 golden **바이트 단위 equality** 비교.
- Domain Track `D-CNV-*` Decimal assert는 **유지** — GM은 Boundary 문자열 위주.

---

## Harness (SSOT)

| 파일 | 역할 |
|------|------|
| `tests/_approval.py` | `assert_matches_golden(actual, relative)` |
| `tests/golden/{name}.approved.txt` | 승인 스냅샷 (수동 편집 **금지**) |
| `tests/conftest.py` | `tests/` on `sys.path` — `from _approval import …` |

### `assert_matches_golden` 계약

- `UPDATE_GOLDEN=1` → golden 파일 **생성·갱신** (팀 승인 후만)
- `UPDATE_GOLDEN` 없음 → 읽기 비교, mismatch 시 diff 포함 `AssertionError`
- golden 파일 없음 → `UPDATE_GOLDEN=1` 실행 안내

---

## 기본 Target — U-OUT-01 (AC-01)

| 항목 | 계약 |
|------|------|
| **입력** | `meter:2.5` |
| **stdout** | PRD §6.1 TEXT 3줄 전문 |
| **POLICY-O01** | 각 줄 `2.5 meter = …` prefix |
| **RG-04** | feet `8.2`, yard `2.7` (1자리 half-up) |
| **golden 경로** | `tests/golden/u_out_01_meter_2_5.approved.txt` |

**승인 스냅샷 예:**

```text
2.5 meter = 2.5 meter
2.5 meter = 8.2 feet
2.5 meter = 2.7 yard

```

---

## 수행 절차 (Steps)

1. **전제 확인** — Target Boundary pytest **PASS** (구현 완료 상태).
2. **Phase 선언** — 필수 선언 형식 출력.
3. **`src/` 미변경** — 로직 수정 **금지**. 테스트·golden·`_approval.py`만.
4. **`tests/_approval.py`** — 없으면 생성 (위 Harness 계약).
5. **테스트 수정** — `tests/boundary/test_u_out_01.py` (또는 지정 Target):
   - `stdin "meter:2.5"` → `stdout` 전체 `assert_matches_golden(stdout, relative)`
   - `exit_code` / `stderr` 보조 assert 유지 가능
   - mock 테스트·integration smoke **동일 golden** 공유 가능
6. **기준 생성** (팀 승인 후):

```powershell
$env:UPDATE_GOLDEN="1"
python -m pytest tests/boundary/test_u_out_01.py -v
Remove-Item Env:UPDATE_GOLDEN
```

7. **검증** (`UPDATE_GOLDEN` **없음**) → **matched** 확인.
8. **보고** — golden 경로 · matched 여부 · diff 요약.

---

## 테스트 예시 (U-OUT-01)

```python
from _approval import assert_matches_golden

_GOLDEN = "u_out_01_meter_2_5.approved.txt"

def test_u_out_01_integration_smoke_meter_2_5() -> None:
    # Given / When: real CliApp, stdin "meter:2.5"
    stdout, stderr, exit_code = app.run("meter:2.5")

    # Then: golden master
    assert exit_code == 0
    assert stderr == ""
    assert_matches_golden(stdout, _GOLDEN)
```

---

## 선택 Target — U-IN stderr golden

| 항목 | 예 |
|------|-----|
| 입력 | `meter:-1` |
| stderr | `Negative value not allowed: -1\n` (E004 §3.5) |
| exit | `4` |
| golden | `tests/golden/u_in_03b_meter_neg1.approved.txt` |

Boundary 오류 경로 회귀용 — **1건 추가 권장**, 필수 아님.

---

## Golden Master 완료 보고

```markdown
## Golden Master 완료

- Target: U-OUT-01 (AC-01)
- Golden: tests/golden/u_out_01_meter_2_5.approved.txt
- UPDATE_GOLDEN: 생성 완료 (팀 승인 기준)
- 검증: matched — UPDATE_GOLDEN 없이 2 passed
- src/: 무변경
- Domain D-CNV-*: 유지 (GM 미적용)
```

---

## 성공 조건

- [ ] `tests/_approval.py` 존재
- [ ] `tests/golden/*.approved.txt` **실행 출력으로만** 생성
- [ ] `UPDATE_GOLDEN` 없이 Target pytest **PASSED** (matched)
- [ ] golden **수동 편집 없음**
- [ ] `src/` **무변경**
- [ ] `D-CNV-*` Decimal assert **삭제·완화 없음**

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **`src/` 로직 변경** | GM = 회귀 고정만 |
| **golden 파일 수동 편집으로 통과** | 승인 우회 |
| **`UPDATE_GOLDEN` 무단 실행** | 팀 승인 후만 |
| **Domain assert를 golden으로 대체** | Dual-Track 분리 |
| **RG-04·POLICY-O01 변경 without PRD** | §8.3 snapshot 절차 |
| **git commit** | 사용자 요청 시만 |
