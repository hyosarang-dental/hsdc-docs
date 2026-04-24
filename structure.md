# hsdc-docs Structure

이 문서는 현재 문서 구조와 스타일 레이어의 기준을 정리합니다. `handoff.md`가 작업 이력과 인수인계 메모라면, 이 문서는 실제 파일을 수정할 때 보는 구조표입니다.

## 1. 사이트 구성

```text
hsdc-docs/
├─ mkdocs.yml
├─ handoff.md
├─ structure.md
├─ scripts/
│  └─ serve.py
└─ docs/
   ├─ index.md
   ├─ certificates.md
   ├─ certificate-fees.md
   ├─ non-covered-fees.md
   ├─ data/
   │  ├─ *-Certificated.csv
   │  ├─ *-Noninsured.csv
   │  └─ certificate-fees.csv
   ├─ javascripts/
   │  └─ fee-count.js
   └─ stylesheets/
      ├─ tokens.css
      ├─ base.css
      ├─ components.css
      ├─ home.css
      ├─ fees.css
      ├─ certificates.css
      └─ extra.css
```

## 2. Markdown Pages

| 파일 | 역할 | 주요 CSS 스코프 |
|---|---|---|
| `docs/index.md` | 문서형 안내 허브. 환자가 먼저 볼 3개 안내 페이지를 순서형 링크로 연결 | `.page-home` |
| `docs/certificates.md` | 치아보험 서류 발급 절차, 준비물, 사전 신청 CTA, 보험사 앱 청구 흐름 | `.page-certificates` |
| `docs/certificate-fees.md` | 제증명서 발급 비용. CSV 4개를 `read_csv()`로 출력 | `.page-fees`, `.fee-table`, `.fee-section` |
| `docs/non-covered-fees.md` | 비급여 수가표. CSV 8개를 `read_csv()`로 출력 | `.page-fees`, `.fee-table`, `.fee-section` |

페이지 전용 UI는 반드시 페이지 루트 스코프 안에 둡니다. 예를 들어 홈 전용 요소는 `.page-home`, 발급 안내 전용 요소는 `.page-certificates`, 비용표 전용 요소는 `.page-fees` 아래에서만 스타일링합니다.

## 3. Stylesheet Layers

`mkdocs.yml`의 `extra_css` 로딩 순서는 아래 기준을 유지합니다.

```yaml
extra_css:
  - stylesheets/tokens.css
  - stylesheets/base.css
  - stylesheets/components.css
  - stylesheets/home.css
  - stylesheets/fees.css
  - stylesheets/certificates.css
```

| 파일 | 책임 |
|---|---|
| `tokens.css` | 폰트 import, Soft Sage 색상 토큰, Material CSS 변수 |
| `base.css` | 전역 타이포그래피, 헤더, 검색, 좌측 네비, 기본 admonition, footer, 스크롤바 |
| `components.css` | 여러 페이지에서 재사용하는 `eyebrow`, `doc-meta`, `quick-jump` |
| `home.css` | 홈 문서 허브 전용 링크 리스트, 안내 라인, 확인 순서 |
| `fees.css` | 수가표 테이블, 가격 열, 섹션 번호, fine print |
| `certificates.css` | 발급 안내 페이지의 PART 구조, key points, CTA, tip line, steps |
| `extra.css` | 레거시 entrypoint 안내만 남긴 빈 호환 파일 |

## 4. Fee Table Contract

수가표는 Markdown에서 각 `read_csv()`를 아래처럼 감쌉니다.

```markdown
## 진단서 { .fee-section }

<div class="fee-table" markdown>

{{ read_csv('Diagnosis-Certificated.csv') }}

</div>
```

규칙:

- `.fee-table`이 있는 표만 수가표 스타일을 받습니다.
- `.fee-section`은 `fee-count.js`가 행 수를 세어 `data-count`를 붙입니다.
- `fee-count.js`는 헤더 텍스트가 `비용`인 열을 찾아 `.price` 클래스를 붙입니다.
- 숫자만 세리프 폰트가 필요할 때 `fee-count.js`가 숫자를 `<span class="num">`으로 감쌉니다.
- 비용 열 CSS는 열 위치 추정 대신 `.price` 클래스만 사용합니다.

## 5. Data And Legacy Files

현재 운영 데이터는 `docs/data/*-Certificated.csv`와 `docs/data/*-Noninsured.csv`입니다.

정리 후보:

- `docs/build_fees.py`
- `docs/hooks/fees_hook.py`
- `docs/data/certificate-fees.csv`

위 파일들은 초기 단일 CSV 방식의 흔적으로 보이며, 현재 `mkdocs.yml`에는 hook 등록이 없습니다. 삭제 전에는 실제 운영에서 참조 중인지 한 번 더 확인합니다.

## 6. Local Verification

빌드 확인:

```bash
.venv/bin/mkdocs build --strict
```

프리뷰 서버:

```bash
.venv/bin/python scripts/serve.py -a 0.0.0.0:8000
```

`8000` 포트가 이미 사용 중이면 다른 포트를 사용합니다.
