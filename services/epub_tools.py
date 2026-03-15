from __future__ import annotations

from pathlib import Path
from typing import Any

from ebooklib import epub

from services.style_templates import get_style_css


def read_text_file_with_fallback(path: str | Path) -> str:
    p = Path(path)
    try:
        return p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return p.read_text(encoding="cp949")


def split_text_into_chapters(text: str, mode: str, delimiter: str | None = None) -> list[tuple[str, str]]:
    src = (text or "").strip()
    if not src:
        return [("Chapter 1", "")]
    if mode == "blankline":
        chunks = [c.strip() for c in __import__("re").split(r"\n\s*\n+", src) if c.strip()]
    elif mode == "delimiter":
        if not delimiter:
            raise ValueError("delimiter 모드에서는 구분 문자열이 필요합니다.")
        chunks = [c.strip() for c in src.split(delimiter) if c.strip()]
    else:
        chunks = [src]
    return [(f"Chapter {i}", c) for i, c in enumerate(chunks, 1)]


def build_epub_from_text(
    title: str,
    author: str,
    language: str,
    text: str,
    split_mode: str,
    delimiter: str | None,
    style_template: str,
    custom_style_options: dict[str, Any] | None,
    source_filename: str | None = None,
):
    safe_title = title.strip() if title else suggest_title_from_filename(source_filename or "untitled.txt")
    safe_author = author.strip() if author else "Unknown"
    safe_lang = language.strip() if language else "ko"

    book = epub.EpubBook()
    book.set_identifier(f"textcraft-{safe_title}")
    book.set_title(safe_title)
    book.set_language(safe_lang)
    book.add_author(safe_author)

    css_text = get_style_css(style_template, custom_style_options)
    style_item = epub.EpubItem(uid="style_nav", file_name="style/style.css", media_type="text/css", content=css_text.encode("utf-8"))
    book.add_item(style_item)

    chapters = split_text_into_chapters(text, split_mode, delimiter)
    epub_chapters = []
    for idx, (chapter_title, content) in enumerate(chapters, 1):
        c = epub.EpubHtml(title=chapter_title, file_name=f"chap_{idx}.xhtml", lang=safe_lang)
        paragraphs = "".join(f"<p>{line}</p>" for line in content.splitlines() if line.strip())
        c.content = f"<h1>{chapter_title}</h1>{paragraphs}"
        c.add_item(style_item)
        book.add_item(c)
        epub_chapters.append(c)

    book.toc = tuple(epub_chapters)
    book.spine = ["nav", *epub_chapters]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    return book


def save_epub(book, output_path: str | Path) -> None:
    epub.write_epub(str(output_path), book, {})


def suggest_title_from_filename(path: str | Path) -> str:
    return Path(path).stem or "Untitled"


def make_output_epub_path(input_path: str | Path, output_dir: str | Path | None = None, overwrite: bool = False) -> Path:
    src = Path(input_path)
    out_dir = Path(output_dir) if output_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    candidate = out_dir / f"{src.stem}.epub"
    if overwrite or not candidate.exists():
        return candidate
    idx = 1
    while True:
        alt = out_dir / f"{src.stem}({idx}).epub"
        if not alt.exists():
            return alt
        idx += 1
