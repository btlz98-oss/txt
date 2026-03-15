from __future__ import annotations

from pathlib import Path
from typing import Any

from services.epub_tools import (
    build_epub_from_text,
    make_output_epub_path,
    read_text_file_with_fallback,
    save_epub,
    suggest_title_from_filename,
)


def filter_unique_paths(paths: list[str | Path]) -> list[Path]:
    seen: set[str] = set()
    out: list[Path] = []
    for p in paths:
        rp = str(Path(p).resolve())
        if rp in seen:
            continue
        seen.add(rp)
        out.append(Path(rp))
    return out


def collect_txt_files_from_paths(paths: list[str | Path], recursive: bool = False) -> list[Path]:
    files: list[Path] = []
    for path in filter_unique_paths(paths):
        if path.is_file() and path.suffix.lower() == ".txt":
            files.append(path)
        elif path.is_dir():
            iterator = path.rglob("*.txt") if recursive else path.glob("*.txt")
            files.extend(iterator)
    return filter_unique_paths(files)


def batch_convert_txt_to_epub(
    paths: list[str | Path],
    output_dir: str | Path | None,
    recursive: bool,
    overwrite: bool,
    common_author: str,
    common_language: str,
    title_prefix: str,
    title_suffix: str,
    split_mode: str,
    delimiter: str | None,
    style_template: str,
    custom_style_options: dict[str, Any] | None,
) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    files = collect_txt_files_from_paths(paths, recursive=recursive)
    for src in files:
        try:
            text = read_text_file_with_fallback(src)
            base_title = suggest_title_from_filename(src)
            title = f"{title_prefix}{base_title}{title_suffix}"
            out_path = make_output_epub_path(src, output_dir, overwrite)
            book = build_epub_from_text(
                title=title,
                author=common_author,
                language=common_language,
                text=text,
                split_mode=split_mode,
                delimiter=delimiter,
                style_template=style_template,
                custom_style_options=custom_style_options,
                source_filename=str(src),
            )
            save_epub(book, out_path)
            results.append({"input": str(src), "output": str(out_path), "status": "성공", "message": "변환 완료"})
        except Exception as exc:
            results.append({"input": str(src), "output": "", "status": "실패", "message": str(exc)})
    return results
