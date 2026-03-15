from __future__ import annotations

import difflib
import html


def _wrap_html(body: str) -> str:
    style = """
    <style>
    body{font-family:Segoe UI, sans-serif; white-space:pre-wrap;}
    .add{background:#d4f8d4;}
    .del{background:#ffd6d6;text-decoration:line-through;}
    .chg{background:#fff3bf;}
    .row{margin:2px 0;padding:2px 4px;border-radius:4px;}
    </style>
    """
    return f"<html><head>{style}</head><body>{body}</body></html>"


def diff_by_line(a: str, b: str) -> str:
    rows = []
    for line in difflib.ndiff((a or "").splitlines(), (b or "").splitlines()):
        cls = "chg"
        if line.startswith("+ "):
            cls = "add"
        elif line.startswith("- "):
            cls = "del"
        rows.append(f"<div class='row {cls}'>{html.escape(line)}</div>")
    return _wrap_html("".join(rows))


def _seq_diff_html(a_tokens: list[str], b_tokens: list[str]) -> str:
    matcher = difflib.SequenceMatcher(a=a_tokens, b=b_tokens)
    parts: list[str] = []
    for op, i1, i2, j1, j2 in matcher.get_opcodes():
        if op == "equal":
            parts.append(html.escape("".join(a_tokens[i1:i2])))
        elif op == "delete":
            parts.append(f"<span class='del'>{html.escape(''.join(a_tokens[i1:i2]))}</span>")
        elif op == "insert":
            parts.append(f"<span class='add'>{html.escape(''.join(b_tokens[j1:j2]))}</span>")
        else:
            old_text = html.escape("".join(a_tokens[i1:i2]))
            new_text = html.escape("".join(b_tokens[j1:j2]))
            parts.append(f"<span class='chg'>[{old_text} → {new_text}]</span>")
    return _wrap_html("<div class='row'>" + "".join(parts) + "</div>")


def diff_by_word(a: str, b: str) -> str:
    return _seq_diff_html((a or "").split(" "), (b or "").split(" "))


def diff_by_char(a: str, b: str) -> str:
    return _seq_diff_html(list(a or ""), list(b or ""))
