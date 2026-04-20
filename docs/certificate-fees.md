<div class="eyebrow">안내 / 제증명서 발급 비용</div>
# 제증명서 발급비용

본원에서 발급 가능한 제증명 서류의 비용을 안내해드립니다.
비용은 의료법에 따른 기준을 준수하여 책정되었습니다.

가격은 변동될 수 있으며, 최신 정보는 내원 시 확인해 주세요.

<div class="doc-meta">LAST UPDATED · 2026.04.15</div>

<div class="quick-jump">
  <a href="#진단서">진단서</a>
  <a href="#영상기록-사본">영상·기록 사본</a>
  <a href="#확인서">확인서</a>
  <a href="#영수-관련">영수 관련</a>
</div>

<!-- ============================================================
     CSV 파일 구성 예시 (docs/data/fees_*.csv):
        category,name,unit,price,note
        진단서,병무용 진단서,1통,20000,
        ...

     각 카테고리별 CSV로 분리하거나, 한 파일로 두고
     아래처럼 필요한 섹션만 read_csv 로 불러옵니다.
     ============================================================ -->

## 진단서 { .fee-section }

{{ read_csv('data/fees_진단서.csv') }}

## 영상·기록 사본 { .fee-section}

{{ read_csv('data/fees_영상기록사본.csv') }}

## 확인서 { .fee-section }

{{ read_csv('data/fees_확인서.csv') }}

## 영수 관련 { .fee-section }

{{ read_csv('data/fees_영수관련.csv') }}

---

→ [제증명서 발급 안내](certificates.md) 페이지에서 서류 발급 절차를 확인하세요.