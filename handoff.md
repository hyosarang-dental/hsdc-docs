# hsdc-docs Handoff

효사랑치과병원 환자용 안내문을 Notion에서 GitHub Pages(MkDocs Material)로 옮긴 프로젝트입니다. 이 문서는 **현재 상태 스냅샷**과 **다음 작업자가 알아야 할 결정/우회**를 정리합니다.

---

## 1. 프로젝트 개요

- **저장소**: `naljahyun/hsdc-docs`
- **사이트 URL**: `https://naljahyun.github.io/hsdc-docs/` (배포 파이프라인 미구성 — §6 참조)
- **로컬 경로**: `/home/head/hsdc-docs/` (Proxmox Linux VM, VS Code Remote-SSH로 편집)
- **대상 페이지 4종** (최상단 왼쪽 네비게이션):
  1. 홈 (`index.md`)
  2. 제증명서 발급 안내 (`certificates.md`)
  3. 제증명서 발급비용 (`certificate-fees.md`)
  4. 비급여 수가표 (`non-covered-fees.md`)

> "재증명서"는 한자 오타(再→諸). 모든 곳에서 "제증명서"로 통일됨.

---

## 2. 기술 스택 (실제 설치·설정 기준)

| 영역 | 사용 중인 것 | 비고 |
|---|---|---|
| SSG | `mkdocs` 1.6.1 | |
| 테마 | `mkdocs-material` 9.7.6 | `palette.scheme: default` (다크모드 비활성) |
| 표 데이터 | `mkdocs-table-reader-plugin` 3.1.0 | CSV → HTML 표. `data_path: docs/data` |
| 슬러그 | `pymdownx.slugs.slugify` | 한글 헤딩 ID 지원 (기본 slugify는 한글 → 빈 슬러그 → `_1`/`_2` 대체) |
| 확장 | `pymdown-extensions` 10.21.2 | emoji(twemoji), tabbed, details, superfences |
| 폰트 (본문) | Pretendard Variable | `--sg-sans` |
| 폰트 (세리프) | Noto Serif KR | `--sg-serif` — 비용 숫자 전용 |
| 폰트 (코드) | JetBrains Mono | `--sg-mono` |

네비게이션 기능: `navigation.top`, `navigation.instant`, `navigation.tracking` (탭은 쓰지 않고 좌측 사이드바만).

---

## 3. 저장소 구조

```text
hsdc-docs/
├─ mkdocs.yml
├─ handoff.md                    # 이 문서
├─ requirements.txt              # (없으면 추가 필요)
├─ .venv/                        # 로컬 가상환경
├─ scripts/
│  └─ serve.py                   # 라이브 리로드 우회 스크립트 — §5 참조
└─ docs/
   ├─ index.md                   # 랜딩
   ├─ certificates.md            # 제증명 발급 안내
   ├─ certificate-fees.md        # 제증명 발급비용 (CSV 4개 로드)
   ├─ non-covered-fees.md        # 비급여 수가표 (CSV 빈 상태)
   ├─ build_fees.py              # (미사용) 초기 단일 CSV → 마크다운 렌더 유틸
   ├─ hooks/fees_hook.py         # (미사용) build_fees.py 연결 훅
   ├─ data/
   │  ├─ fees_진단서.csv             # 서류명,단위,비용,비고 (8행)
   │  ├─ fees_영상기록사본.csv         # 〃 (5행)
   │  ├─ fees_확인서.csv             # 〃 (2행)
   │  ├─ fees_영수관련.csv           # 〃 (3행)
   │  ├─ non-covered-fees.csv    # 대분류,소분류,단위,비용 (헤더만)
   │  └─ certificate-fees.csv    # (미사용 레거시)
   ├─ javascripts/
   │  └─ fee-count.js            # h2.fee-section 데코 + 비용 컬럼 처리 — §4
   └─ stylesheets/
      └─ extra.css               # Soft Sage 디자인 시스템
```

### 3.1 CSV 스키마

- **제증명 4종** (`fees_*.csv`): `서류명,단위,비용,비고`
- **비급여** (`non-covered-fees.csv`): `대분류,소분류,단위,비용`
- 비용 포맷: `"20,000원"` 문자열 (쉼표 포함). 무료는 `무료`, 비고 없으면 `—`.
- **알려진 이슈**: `fees_영수관련.csv`의 `동의 확인서`는 초기 핸드오프 자료의 `통원 확인서`와 다름. 실제 병원 운영 용어 확인 필요.

### 3.2 미사용 자산 (정리 후보)

- `docs/build_fees.py`, `docs/hooks/fees_hook.py` — 초기 단일 `fees.csv` 접근 방식. 현재는 카테고리별 CSV + table-reader를 쓰므로 미사용. `mkdocs.yml`에 훅 등록 안 됨.
- `docs/data/certificate-fees.csv` — 이전 통합 CSV 레거시.
- 정리 기준 결정 후 삭제 권장.

---

## 4. 아키텍처 메모 — 몇 가지 중요한 우회

### 4.1 table-reader 인라인 `text-align` 이슈

`mkdocs-table-reader-plugin`이 모든 `<td>`에 `style="text-align: left;"`를 강제로 박습니다. 인라인 스타일은 외부 CSS를 이기므로 `.md-typeset td { text-align: right }` 같은 규칙이 **조용히 실패**합니다.

**우회**: `docs/javascripts/fee-count.js`가 페이지 로드 시 헤더 텍스트가 `비용`인 열을 찾아 td의 인라인 스타일을 제거하고 `.price` 클래스를 부여합니다. CSS는 `th.price, td.price`를 대상으로 정렬을 걸면 됩니다.

### 4.2 비용 셀 — 숫자만 세리프

요구사항: `20,000원`의 숫자는 Noto Serif KR, `원`은 본문 폰트(Pretendard) 유지.

**구현**: 같은 `fee-count.js`가 `.price` 셀 내부 텍스트 노드를 훑어 `[0-9][0-9,]*` 패턴을 `<span class="num">`으로 래핑. CSS `.num { font-family: var(--sg-serif) }`만 적용 — 주변 텍스트는 영향 없음.

### 4.3 섹션 카운터와 번호

`## 제목 { .fee-section }`만 붙이면:
- JS가 `tbody tr` 개수를 세어 `data-count` 속성 세팅 → CSS `::after`가 "8 items" 출력
- CSS `counter-increment`로 `01`, `02` 자동 번호
- 마크다운에 수동 숫자 쓰지 말 것.

### 4.4 한글 헤딩 앵커

기본 `toc` 확장은 한글을 슬러그화하지 못해 빈 결과 → `_1`, `_2`로 떨어집니다. `mkdocs.yml`에서:

```yaml
- toc:
    permalink: true
    slugify: !!python/object/apply:pymdownx.slugs.slugify {kwds: {case: lower}}
```

quick-jump 앵커(`<a href="#진단서">` 등)는 이 슬러그와 **정확히** 일치해야 함. 수정 시 `grep -oE 'id="[^"]*"' site/.../index.html`로 확인.

### 4.5 디자인 시스템 — Soft Sage

`extra.css` 최상단에 토큰 정의:
- `--sg-bg`, `--sg-ink`, `--sg-muted`, `--sg-accent`, `--sg-accent-soft`, `--sg-table-head` 등
- 커스텀 UI 유틸 클래스:
  - `.eyebrow` — 페이지 상단 작은 카테고리 라벨
  - `.doc-meta` — "LAST UPDATED · YYYY.MM.DD" 등 메타 라인
  - `.quick-jump` — 페이지 내 앵커 바로가기 그룹
  - `.fee-section` — 번호·카운트 달린 h2
  - `.key-points` — certificates 페이지 4칸 안내 박스
  - `.price` / `.num` — JS가 부여하는 비용 셀용

라이트 모드 단일 팔레트. 오른쪽 TOC 사이드바는 전역 숨김(`.md-sidebar--secondary { display: none }`) — 페이지마다 `.quick-jump`로 직접 네비 제공하기 때문.

---

## 5. 로컬 개발

### 5.1 환경 재구축

```bash
cd /home/head/hsdc-docs
python -m venv .venv
.venv/bin/pip install mkdocs-material mkdocs-table-reader-plugin
```

(가능하면 `requirements.txt`를 추가해서 버전 고정할 것.)

### 5.2 프리뷰 서버 — `scripts/serve.py` 필요

**중요**: `.venv/bin/mkdocs serve`의 라이브 리로드가 이 환경에서 작동하지 않습니다. mkdocs 1.6의 `PollingObserver`가 VS Code Remote-SSH의 원자 저장 + 폴링 사이클과 맞지 않아, 파일 변경이 감지되지만 `server.watch()`가 호출되지 않는 현상. 대신:

```bash
.venv/bin/python scripts/serve.py -a 0.0.0.0:8000
```

VM 호스트에서 `http://<VM-IP>:8000/hsdc-docs/` 로 접속. `scripts/serve.py`는 mkdocs 내부 `LiveReloadServer`를 직접 와이어링해서 watch를 등록합니다.

### 5.3 Strict 빌드 확인

```bash
.venv/bin/mkdocs build --strict
```

(Material 팀의 MkDocs 2.0 마케팅 배너는 무시해도 됨.)

---

## 6. 미완·예정

- [ ] **GitHub Pages 배포 파이프라인** — `.github/workflows/ci.yml` 미구성. `mkdocs gh-deploy --force`를 사용하는 표준 워크플로 추가 필요.
- [ ] **`non-covered-fees.csv` 데이터 입력** — 대분류/소분류 미결정. 데이터 받으면 추가.
- [ ] **레거시 파일 정리** — `docs/build_fees.py`, `docs/hooks/fees_hook.py`, `docs/data/certificate-fees.csv`.
- [ ] **서류명 확인** — `동의 확인서` vs `통원 확인서` (§3.1).
- [ ] **requirements.txt 작성** — 현재 수동 pip install에 의존.
- [ ] **사전 신청서 링크** — `certificates.md`의 CTA 버튼이 `#` 더미. 실제 폼 URL 확정 시 교체.

---

## 7. 작업 원칙 (합의된 기조)

- 디자인은 "깔끔한 문서형 안내 페이지". 랜딩·브로셔 느낌 지양.
- 여백·가독성·모바일 우선.
- 불필요한 컬러/효과 최소화. 강조 박스는 제한된 종류만.
- 커밋은 기능 단위로 분리. 각 커밋 메시지 끝에 `Co-Authored-By: Claude Opus 4.7` 라인 유지.
- 파일 수정은 로컬 → 커밋 → push. 디자인 이터레이션을 claude.ai에서 돌릴 경우 결과를 이 세션으로 다시 가져와서 반영.

---

## 8. 최근 주요 커밋 (참고)

```
1eb0e18 docs: refine certificates copy and index label
3e45ac1 feat: serif numerals and auto-aligned price column
e6b6806 fix: enable Korean slugs for heading anchors
1021c26 fix: rename 재증명서 to 제증명서 across nav and handoff doc
94d34da refactor: large design pass on landing and certificates page
b4059fb refactor: iterate site copy, CSV schema, and style
3337e11 feat: add category fee CSVs and legacy markdown hook
91ebfcf feat: apply Soft Sage redesign and fee-count script
adbcb74 feat: scaffold MkDocs Material site with patient guide content
```
