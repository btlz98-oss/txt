from __future__ import annotations

from typing import Any


def get_style_template_names() -> list[str]:
    return ["기본형", "소설형", "에세이형", "웹문서형", "아동도서형", "사용자 정의형"]


def build_default_templates() -> dict[str, str]:
    return {
        "기본형": "h1{font-size:1.6em;font-weight:bold;margin:1.2em 0 0.8em 0;text-align:left;} p{font-size:1em;line-height:1.7;margin-bottom:0.8em;text-indent:1em;}",
        "소설형": "h1{font-size:1.8em;font-weight:bold;text-align:center;margin-top:2em;margin-bottom:2em;} p{line-height:1.8;text-indent:1.6em;margin-bottom:0.6em;} p:first-of-type{text-indent:0;}",
        "에세이형": "h1{font-size:1.5em;font-weight:600;text-align:left;margin:1em 0 0.7em 0;} p{line-height:1.9;margin-bottom:0.9em;text-indent:0;}",
        "웹문서형": "h1{font-size:2.0em;font-weight:bold;text-align:left;margin:1.1em 0 0.7em 0;} p{line-height:1.8;margin-bottom:1.1em;text-indent:0;}",
        "아동도서형": "h1{font-size:2.1em;font-weight:bold;text-align:center;margin:1.3em 0 0.9em 0;} p{line-height:2.0;margin-bottom:1.2em;text-indent:0;}",
    }


def _build_custom_css(custom_options: dict[str, Any] | None = None) -> str:
    opts = custom_options or {}
    return (
        "h1{" f"font-size:{opts.get('title_size','1.6em')};"
        f"text-align:{opts.get('title_align','left')};"
        f"font-weight:{opts.get('title_weight','bold')};"
        f"margin-top:{opts.get('title_margin_top','1.2em')};"
        f"margin-bottom:{opts.get('title_margin_bottom','0.8em')};"
        "}"
        "p{" f"font-size:{opts.get('body_size','1em')};"
        f"line-height:{opts.get('line_height','1.8')};"
        f"text-indent:{opts.get('text_indent','1em')};"
        f"margin-bottom:{opts.get('paragraph_margin_bottom','0.8em')};" "}"
    )


def get_style_css(template_name: str, custom_options: dict[str, Any] | None = None) -> str:
    templates = build_default_templates()
    if template_name == "사용자 정의형":
        return _build_custom_css(custom_options)
    return templates.get(template_name, templates["기본형"])
