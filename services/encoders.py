from __future__ import annotations

import html
from urllib.parse import quote, unquote


def html_escape_text(text: str) -> str:
    return html.escape(text or "")


def html_unescape_text(text: str) -> str:
    return html.unescape(text or "")


def url_encode_text(text: str) -> str:
    return quote(text or "")


def url_decode_text(text: str) -> str:
    return unquote(text or "")
