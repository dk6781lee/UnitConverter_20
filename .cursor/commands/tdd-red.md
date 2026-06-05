---
description: TDD RED — 실패 테스트만 작성, tests/만 수정, pytest FAIL 확인
---

# TDD RED — 실패 테스트 먼저

UnitConverter_20 **BCE + Dual-Track TDD** — **RED 단계만** 수행한다.  
**근거:** `.cursorrules` · `docs/PRD.md` §10 (Test ID C2C)

---

## 필수 선언

응답 **첫 줄**에 반드시 출력:

```
Phase: red | Layer: entity|control|boundary|data | Track: Domain|Boundary|Data | Target: D-*|U-*
```

---

## 목적 (Objective)

- **하나의** 실패 테스트를 `tests/`에 먼저 작성한다.
- `pytest`로 **의도된 FAIL**을 확인한다.
- 프로덕션 코드(`src/`, `UnitConverter.py`)는 **수정하지 않는다**.
- GREEN·REFACTOR는 **별도 Phase**에서 수행한다.

---

## Track · Layer · 파일 매핑

| Track | Layer | 테스트 경로 | Test ID | Mock |
|-------|-------|-------------|---------|------|
| **Domain** | entity, control | `tests/domain/test_d_*.py` | `D-*` | Domain Mock **금지** |
| **Boundary** | boundary | `tests/boundary/test_u_*.py` | `U-*` (`U-IN`, `U-OUT`) | Service/Registry Mock **허용** |
| **Data** | data | `tests/data/test_d_cfg_*.py` | `D-CFG-*` | temp files only |

**Assert 분리:** 환산 정밀도 → `D-CNV-*`. `8.2 feet` 문자열 → `U-OUT-*` only.

---

## 수행 절차 (Steps)

1. **Target 확정** — `docs/PRD.md` §10에서 Test ID 선택. 미지정 시 해당 Track **다음 ID**.
2. **Phase 선언** — 필수 선언 형식 출력.
3. **AAA 테스트 1건** — `tests/`만 수정.
   - **Arrange:** Given·실제 domain 객체 (Domain Track: Mock 금지)
   - **Act:** 검증 대상 API/CLI 호출
   - **Assert:** PRD 계약 **엄격** (Given-When-Then docstring 권장)
4. **`src/` 미수정** — import 대상 없으면 ImportError도 RED로 보고 가능.
5. **pytest 단일 실행** — Target 테스트 1개.
6. **FAIL 확인** — **FAILED** 필수. PASS면 assert·기대값 재검토.
7. **보고** — 아래 형식. **GREEN 하지 않음.**

---

## pytest 예시 (bash)

```bash
# Domain
pytest tests/domain/test_d_cnv_01.py::test_d_cnv_01_meter_hub -q

# Boundary
pytest tests/boundary/test_u_out_01.py::test_u_out_01_text_snapshot -q

# Data
pytest tests/data/test_d_cfg_01.py::test_d_cfg_01a_valid_config -q
```

---

## RED 완료 보고

```markdown
## RED 완료

- Target: D-CNV-01
- pytest: FAILED — AssertionError: …
- 변경 파일: tests/domain/test_d_cnv_01.py (tests/만)
- Mock: Domain Track — 없음
- 다음: GREEN — src/entity 최소 구현
```

---

## 성공 조건

- [ ] Target 테스트 **1개**만 추가·수정
- [ ] pytest 결과 = **FAILED**
- [ ] 변경 = **`tests/`만**
- [ ] Domain Track → Domain Mock **미사용**
- [ ] skip / xfail / assert 완화 **없음**
- [ ] `src/` **무변경**

---

## 금지 사항

| 금지 | 이유 |
|------|------|
| **`src/` · `UnitConverter.py` 수정** | RED = 테스트만 |
| **Domain Track Mock** | `unittest.mock`, Registry·ConversionService patch 금지 |
| **assert 완화·제거·skip·xfail** | GREEN 우회 |
| **한 턴에 여러 RED** | 1 FAIL = 1 RED |
| **GREEN / REFACTOR 선행** | RED → GREEN 순서 |
| **git commit** | 사용자 요청 시만 |
