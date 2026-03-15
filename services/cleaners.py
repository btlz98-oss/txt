from __future__ import annotations

import re
from typing import Iterable

BRACKET_PAIRS = [
    ("(", ")"), ("[", "]"), ("{", "}"), ("<", ">"),
    ("（", "）"), ("［", "］"), ("｛", "｝"), ("〈", "〉"),
    ("《", "》"), ("「", "」"), ("『", "』"), ("【", "】"),
]


def remove_bracket_contents(text: str, bracket_types: Iterable[tuple[str, str]] | None = None) -> str:
    """괄호와 괄호 내부 내용을 제거한다. 중첩은 간단한 스택 처리로 대응."""
    if not text:
        return ""
    pairs = list(bracket_types or BRACKET_PAIRS)
    openers = {o for o, _ in pairs}
    closer_to_opener = {c: o for o, c in pairs}
    opener_stack: list[str] = []
    output: list[str] = []
    for ch in text:
        if ch in openers:
            opener_stack.append(ch)
            continue
        if ch in closer_to_opener:
            if opener_stack and opener_stack[-1] == closer_to_opener[ch]:
                opener_stack.pop()
            continue
        if not opener_stack:
            output.append(ch)
    return "".join(output)


def remove_english(text: str) -> str:
    return re.sub(r"[A-Za-z]", "", text or "")


def remove_hanja(text: str) -> str:
    """기본 한자 영역과 일부 확장 영역 제거."""
    if not text:
        return ""
    pattern = r"[\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF\U00020000-\U0002A6DF\U0002A700-\U0002EBEF]"
    return re.sub(pattern, "", text)


def remove_special_chars(text: str, mode: str = "basic", allowed_punctuation: str | None = None) -> str:
    """특수문자 정리 모드: basic/strict/custom_punctuation."""
    if not text:
        return ""
    if mode == "strict":
        return re.sub(r"[^0-9가-힣\s]", "", text)
    if mode == "custom_punctuation":
        punct = re.escape(allowed_punctuation or "")
        return re.sub(rf"[^0-9A-Za-z가-힣\s{punct}]", "", text)
    return re.sub(r"[^0-9A-Za-z가-힣\s\.,!?]", "", text)


def merge_intraline_breaks(text: str) -> str:
    """문단 내부 개행은 공백으로 합치고 빈 줄은 문단 경계로 유지."""
    if not text:
        return ""
    blocks = re.split(r"\n\s*\n+", text.strip())
    merged = [re.sub(r"\s*\n\s*", " ", b).strip() for b in blocks if b.strip()]
    return "\n\n".join(merged)


def collapse_blank_lines(text: str) -> str:
    return re.sub(r"\n{2,}", "\n", text or "")


def normalize_spaces(text: str) -> str:
    return re.sub(r"[ \t]{2,}", " ", text or "")


def trim_lines(text: str) -> str:
    if not text:
        return ""
    return "\n".join(line.strip() for line in text.splitlines()).strip()


def apply_cleanup_pipeline(text: str, options: dict) -> str:
    """옵션 순서대로 문단 정리 파이프라인 실행."""
    result = text or ""
    if options.get("remove_brackets"):
        result = remove_bracket_contents(result)
    if options.get("remove_english"):
        result = remove_english(result)
    if options.get("remove_hanja"):
        result = remove_hanja(result)
    if options.get("remove_special"):
        result = remove_special_chars(
            result,
            mode=options.get("special_mode", "basic"),
            allowed_punctuation=options.get("allowed_punctuation"),
        )
    if options.get("merge_intraline_breaks"):
        result = merge_intraline_breaks(result)
    if options.get("collapse_blank_lines"):
        result = collapse_blank_lines(result)
    if options.get("trim_lines"):
        result = trim_lines(result)
    if options.get("normalize_spaces"):
        result = normalize_spaces(result)
    return result
