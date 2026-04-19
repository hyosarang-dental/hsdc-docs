"""
MkDocs hook — 빌드할 때 {{ fees_table }} 를 fees.csv 기반 마크다운으로 치환.
mkdocs.yml 에 아래 추가:
    hooks:
      - hooks/fees_hook.py
"""
from pathlib import Path
import sys

# 프로젝트 루트의 build_fees.py 를 import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build_fees import build_markdown


def on_page_markdown(markdown, page, config, files):
    if "{{ fees_table }}" not in markdown:
        return markdown
    return markdown.replace("{{ fees_table }}", build_markdown())
