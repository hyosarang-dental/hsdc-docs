# Codex Handoff

## 프로젝트 개요

노션의 공개 페이지를 GitHub Pages 기반의 정적 사이트로 이전한다. 목적은 환자용 안내 페이지를 더 깔끔하고 빠르게, 그리고 병원 브랜드에 맞게 보여주는 것이다.

현재 우선 대상은 아래 3개다.

- 환자 재증명서 발급 안내
- 재증명서 발급비용
- 비급여 수가표

이번 1차 작업에서는 먼저 아래 노션 페이지를 MkDocs Material 사이트의 첫 페이지로 옮긴다.

- 원본 URL: `https://hyosarang.notion.site/2d8f1ee7f7e880a9b919c2a75e27d469`
- 페이지 제목: `치아보험 서류 발급 및 청구 가이드`

## 목표

1. MkDocs Material 기반의 GitHub Pages 사이트 뼈대를 만든다.
2. 위 노션 페이지를 Markdown 문서로 옮긴다.
3. 제증명 발급 비용은 표 형태로 보기 좋게 정리한다.
4. 모바일에서도 읽기 쉽도록 구성한다.
5. 이후 `비급여 수가표`와 다른 안내문을 쉽게 추가할 수 있는 구조로 만든다.

## 핵심 방향

- 노션은 원본 작성 도구로 유지 가능
- GitHub Pages는 공개용 프론트로 사용
- 초기에는 자동 동기화하지 않음
- 먼저 수동 반영 방식으로 안정화
- 디자인은 병원 홈페이지 느낌보다 `깔끔한 문서형 안내 페이지` 방향
- 과한 효과보다 가독성, 여백, 모바일 대응 우선

## 기술 선택

- 정적 사이트 생성기: `MkDocs`
- 테마: `Material for MkDocs`
- 호스팅: `GitHub Pages`
- 배포 방식: 우선 `GitHub Actions` 자동 배포 권장
- 작성 언어: `Markdown`
- 표 데이터: 초기에는 Markdown 표 또는 간단한 HTML
- 추후 표가 커지면 CSV/JSON 분리 고려

## 추천 저장소 구조

```text
project-root/
├─ mkdocs.yml
├─ docs/
│  ├─ index.md
│  ├─ certificates.md
│  ├─ certificate-fees.md
│  ├─ non-covered-fees.md
│  └─ stylesheets/
│     └─ extra.css
└─ .github/
   └─ workflows/
      └─ ci.yml
```

## 이번 단계에서 Codex가 해야 할 일

### 1. MkDocs 프로젝트 초기화

실행 순서:

```bash
mkdir dental-docs
cd dental-docs
python -m venv .venv
source .venv/bin/activate
pip install "mkdocs-material==9.*"
mkdocs new .
```

### 2. `mkdocs.yml` 작성

초기 초안:

```yaml
site_name: 효사랑 안내문
site_url: https://YOUR_USERNAME.github.io/dental-docs/

theme:
  name: material
  language: ko
  features:
    - navigation.tabs
    - navigation.top
    - search.suggest
    - search.highlight
    - content.code.copy

repo_url: https://github.com/YOUR_USERNAME/dental-docs
repo_name: dental-docs

extra_css:
  - stylesheets/extra.css

nav:
  - 홈: index.md
  - 재증명서 발급 안내: certificates.md
  - 재증명서 발급비용: certificate-fees.md
  - 비급여 수가표: non-covered-fees.md
```

> `YOUR_USERNAME`은 실제 GitHub 계정명으로 교체.

### 3. 문서 파일 생성

필수 파일:

- `docs/index.md`
- `docs/certificates.md`
- `docs/certificate-fees.md`
- `docs/non-covered-fees.md`
- `docs/stylesheets/extra.css`

### 4. 홈 화면 작성

`docs/index.md`는 아래 성격으로 작성:

- 병원 환자용 안내문 허브
- 3개 페이지 링크 제공
- 문서형 소개 문구
- 군더더기 없는 레이아웃

예시:

```md
# 효사랑 안내문

환자용 안내 페이지입니다.

- 재증명서 발급 안내
- 재증명서 발급비용
- 비급여 수가표
```

### 5. 노션 페이지를 `certificates.md`로 옮기기

노션 원본 페이지에서 확인된 주요 구조는 아래와 같다.

#### 제목

- 치아보험 서류 발급 및 청구 가이드

#### 도입 문구

- 치아보험 청구를 위한 제증명 발급 절차와 비용 안내
- 병원 내 보험사별 청구 양식 구비 안내
- 방문 전 필수 안내 확인 요청

#### 필독 안내 박스

핵심 문장:

1. 시간이 걸림
2. 미리 신청 권장
3. 신분증 필수

#### 사전 신청 안내 박스

- 지금 신청하면 내원 시 서류 준비 시간 단축 가능
- `서류 발급 사전 신청서 작성하기` 링크 존재
- 실제 링크는 아직 확정 전이면 임시 placeholder 사용

#### 섹션 1

- 제목: `제증명 발급 비용 안내 (의료법 준수)`
- 내용: 발급받으실 서류의 비용을 미리 확인하세요.

#### 섹션 2

- 제목: `서류 발급 신청 시 유의사항`
- 내용 요지:
  - 발급 타이밍: 치료 종료 후 한 번에 발급 권장
  - 서류 수령 방법 중요
  - 환자 본인 방문
  - 가족 대리 방문
  - 제3자 대리 방문

> 원문에는 대리 수령 관련 토글 블록이 있다. 이 내용은 1차 버전에서는 `추후 상세 작성 예정`으로 둘지, 노션 원문을 그대로 풀어쓸지 선택해서 반영.

#### 섹션 3

- 제목: `간편하게 보험 청구하기 (Tip)`
- 내용 요지:
  1. 병원에서 서류 수령
  2. 보험사 앱 실행 후 청구 메뉴 선택
  3. 휴대폰 카메라로 서류 촬영 후 업로드

### 6. `certificate-fees.md` 작성

이 페이지는 비용 안내 전용 페이지다.

초기에는 아래 표를 Markdown 표로 넣고, 나중에 필요하면 카드형/CSV형으로 바꾼다.

## 제증명 발급 비용 데이터

아래 항목은 현재 노션 페이지에서 확인된 데이터다.

| 서류명 | 비용 | 단위 | 분류 |
|---|---:|---|---|
| 병무용 진단서 | 20,000원 | 1통 | 유료(특수) |
| 상해 진단서 (3주 미만) | 50,000원 | 1통 | 유료(특수) |
| 상해 진단서 (3주 이상) | 100,000원 | 1통 | 유료(특수) |
| 장애 진단서 | 15,000원 | 1통 | 유료(특수) |
| 향후치료비 추정서 (1천만원 미만) | 50,000원 | 1통 | 유료(특수) |
| 향후치료비 추정서 (1천만원 이상) | 100,000원 | 1통 | 유료(특수) |
| 영상 사본 (CBCT) | 30,000원 | 1회 | 유료(영상) |
| 영상 사본 (치근단) | 1,500원 | 1장당 | 유료(영상) |
| 영상 사본 (파노라마) | 5,000원 | 1장당 | 유료(영상) |
| 진료기록 사본 (기본 1~5매) | 1,000원 | 1장당 | 유료(사본) |
| 진료기록 사본 (추가 6매부터) | 100원 | 1장당 | 유료(사본) |
| 보험회사 치료 확인서 | 3,000원 | 1통 | 유료(일반) |
| 수술/진료 확인서 | 3,000원 | 1통 | 유료(일반) |
| 일반 진단서 | 10,000원 | 1통 | 유료(일반) |
| 진료비 영수증 | 0원 | 발급 건당 | 무료(기본) |
| 통원 확인서 | 0원 | 1통 | 무료(기본) |
| 진료비 세부내역서 | 0원 | 발급 건당 | 무료(기본) |

### 7. `non-covered-fees.md`는 임시 페이지로 생성

현재 실제 데이터는 아직 미반영 상태다.

초기 문안 예시:

```md
# 비급여 수가표

비급여 항목과 금액을 안내드립니다.

현재 정리 중입니다.
```

이후 실제 표가 확정되면 별도 데이터로 넣는다.

### 8. CSS 최소 보정

`docs/stylesheets/extra.css`에 아래 정도만 먼저 넣는다.

```css
.md-typeset h1 {
  font-weight: 800;
}

.md-typeset table {
  font-size: 0.95rem;
}
```

원장 의도:

- 화려한 랜딩페이지 느낌 아님
- 병원 문서처럼 또딱딱하지도 않게
- 여백 넉넉하게
- 모바일 가독성 우선

### 9. 로컬 미리보기

```bash
mkdocs serve
```

확인 항목:

- 상단 내비게이션 정상 동작
- 한글 글꼴 표시 문제 없는지
- 모바일 폭에서 표가 지나치게 깨지지 않는지
- 링크 구조 자연스러운지

### 10. GitHub 연결 및 배포

```bash
git init
git add .
git commit -m "Initial MkDocs Material site"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dental-docs.git
git push -u origin main
```

그 다음 `.github/workflows/ci.yml` 추가:

```yaml
name: ci

on:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure Git Credentials
        run: |
          git config user.name github-actions[bot]
          git config user.email 41898282+github-actions[bot]@users.noreply.github.com

      - uses: actions/setup-python@v5
        with:
          python-version: 3.x

      - run: echo "cache_id=$(date --utc '+%V')" >> $GITHUB_ENV

      - uses: actions/cache@v4
        with:
          key: mkdocs-material-${{ env.cache_id }}
          path: ~/.cache
          restore-keys: |
            mkdocs-material-

      - run: pip install mkdocs-material

      - run: mkdocs gh-deploy --force
```

## 디자인 원칙

- 배경은 밝게
- 글자는 선명하게
- 컬러는 최소화
- 강조 박스는 1~2종류만 사용
- 표는 과한 색칠 금지
- 환자가 모바일에서 바로 이해할 수 있어야 함

## 열어둘 결정 사항

아직 확정 안 된 것:

- GitHub 저장소 이름
- 실제 GitHub 사용자명
- 사전 신청서 링크 URL
- 비급여 수가표 원본 데이터
- 커스텀 도메인 사용 여부

## 권장 우선순위

1. MkDocs 사이트 생성
2. `치아보험 서류 발급 및 청구 가이드` 이전
3. 비용표 분리 페이지 작성
4. GitHub Pages 배포 성공 확인
5. 모바일 화면 조정
6. 비급여 수가표 추가

## 이번 handoff의 목적

Codex는 여기서부터 바로 실행하면 된다.

가장 먼저 해야 할 것은 아래 3가지다.

1. MkDocs Material 프로젝트 생성
2. 위 문서 구조대로 파일 생성
3. 노션 페이지 내용을 Markdown으로 정리해서 첫 배포본 완성

## 완료 기준

아래 조건을 만족하면 1차 완료로 본다.

- GitHub Pages 주소 접속 가능
- 상단 메뉴 4개 표시
- `재증명서 발급 안내` 페이지 내용 표시
- `재증명서 발급비용` 페이지 표 표시
- 모바일에서도 제목/문단/표가 읽을 만한 수준
- 이후 문서 추가가 쉬운 구조

