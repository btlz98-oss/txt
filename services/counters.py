from __future__ import annotations

import re


def count_text_stats(text: str) -> dict[str, int]:
    """기본 계산 방식 기준 통계를 반환한다."""
    txt = text or ""
    lines = txt.splitlines()
    non_empty_lines = [l for l in lines if l.strip()]
    paragraphs = [p for p in re.split(r"\n\s*\n+", txt.strip()) if p.strip()] if txt.strip() else []
    words = re.findall(r"[A-Za-z0-9가-힣]+", txt)
    return {
        "chars_with_space": len(txt),
        "chars_without_space": len(re.sub(r"\s", "", txt)),
        "line_count": len(lines),
        "line_count_non_empty": len(non_empty_lines),
        "word_count": len(words),
        "paragraph_count": len(paragraphs),
    }
