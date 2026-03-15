from __future__ import annotations


def remove_empty_lines(text: str) -> str:
    return "\n".join(line for line in (text or "").splitlines() if line.strip())


def remove_linebreaks(text: str, replace_with_space: bool = True) -> str:
    repl = " " if replace_with_space else ""
    return (text or "").replace("\r\n", "\n").replace("\n", repl)


def add_linebreak_by_delimiter(text: str, delimiter: str) -> str:
    if not delimiter:
        return text or ""
    return (text or "").replace(delimiter, f"{delimiter}\n")


def remove_linebreak_near_delimiter(text: str, delimiter: str) -> str:
    if not delimiter:
        return text or ""
    return (text or "").replace(f"{delimiter}\n", delimiter).replace(f"\n{delimiter}", delimiter)


def sort_lines(
    text: str,
    reverse: bool = False,
    numeric: bool = False,
    ignore_case: bool = True,
    strip_for_sort: bool = True,
) -> str:
    lines = (text or "").splitlines()

    def base(v: str) -> str:
        return v.strip() if strip_for_sort else v

    try:
        if numeric and all(base(x).replace(".", "", 1).isdigit() for x in lines if base(x)):
            key = lambda x: float(base(x) or 0)
        else:
            key = (lambda x: base(x).lower()) if ignore_case else base
        return "\n".join(sorted(lines, key=key, reverse=reverse))
    except Exception:
        return "\n".join(lines)


def unique_lines(
    text: str,
    preserve_order: bool = True,
    ignore_blank: bool = False,
    case_sensitive: bool = True,
) -> str:
    lines = (text or "").splitlines()
    seen: set[str] = set()
    out: list[str] = []

    def norm(line: str) -> str:
        return line if case_sensitive else line.lower()

    src = lines if preserve_order else sorted(lines)
    for line in src:
        if ignore_blank and not line.strip():
            continue
        token = norm(line)
        if token in seen:
            continue
        seen.add(token)
        out.append(line)
    return "\n".join(out)
