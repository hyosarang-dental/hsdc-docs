#!/usr/bin/env python3
"""
fees.csv 하나를 읽어 카테고리별 마크다운 테이블로 분리해주는 유틸.
사용처 — hooks 혹은 빌드 전 스크립트.

CSV 컬럼: category, name, unit, price, note
출력 컬럼: 서류명 | 단위 | 비용 | 비고  (category 는 제목으로만 사용)
"""
from pathlib import Path
import csv
from collections import OrderedDict

SRC = Path(__file__).parent / "data" / "fees.csv"


def _row_md(r):
    name = r["name"].strip()
    unit = r["unit"].strip() or "—"
    price = r["price"].strip() or "—"
    note = r["note"].strip() or "—"
    return f"| {name} | {unit} | {price} | {note} |"


def build_markdown(src: Path = SRC) -> str:
    groups = OrderedDict()
    with src.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            groups.setdefault(r["category"], []).append(r)

    out = []
    # 바로가기
    out.append('<div class="quick-jump">')
    for cat in groups:
        anchor = cat.replace(" ", "-").replace("·", "").replace("/", "")
        out.append(f'  <a href="#{anchor}">{cat}</a>')
    out.append("</div>")
    out.append("")

    # 카테고리별 테이블
    for cat, rows in groups.items():
        out.append(f'## {cat} {{ .fee-section data-count="{len(rows)}" }}')
        out.append("")
        out.append("| 서류명 | 단위 | 비용 | 비고 |")
        out.append("|---|---|---:|---|")
        for r in rows:
            out.append(_row_md(r))
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    print(build_markdown())
