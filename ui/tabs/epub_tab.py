from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QFileDialog,
    QComboBox, QPlainTextEdit, QMessageBox
)

from services.epub_tools import (
    read_text_file_with_fallback, build_epub_from_text, save_epub, make_output_epub_path, suggest_title_from_filename
)
from services.style_templates import get_style_template_names, get_style_css
from ui.widgets import DropArea


class EpubTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        self.current_txt_paths: list[str] = []

        root = QVBoxLayout(self)
        top = QHBoxLayout()
        self.file_path = QLineEdit(); self.file_path.setPlaceholderText("TXT 파일 경로(여러 개 가능)")
        pick = QPushButton("파일 선택")
        top.addWidget(self.file_path); top.addWidget(pick)
        root.addLayout(top)

        self.drop = DropArea("TXT 파일 드롭")
        root.addWidget(self.drop)

        m1 = QHBoxLayout()
        self.title = QLineEdit(); self.title.setPlaceholderText("제목(비우면 파일명 자동)")
        self.author = QLineEdit(); self.author.setPlaceholderText("저자(비우면 Unknown)")
        self.language = QLineEdit("ko")
        m1.addWidget(QLabel("제목")); m1.addWidget(self.title)
        m1.addWidget(QLabel("저자")); m1.addWidget(self.author)
        m1.addWidget(QLabel("언어")); m1.addWidget(self.language)
        root.addLayout(m1)

        m2 = QHBoxLayout()
        self.split_mode = QComboBox(); self.split_mode.addItems(["single", "blankline", "delimiter"])
        self.delimiter = QLineEdit(); self.delimiter.setPlaceholderText("delimiter 모드 구분 문자열")
        self.template = QComboBox(); self.template.addItems(get_style_template_names())
        m2.addWidget(QLabel("분리 방식")); m2.addWidget(self.split_mode)
        m2.addWidget(QLabel("구분 문자열")); m2.addWidget(self.delimiter)
        m2.addWidget(QLabel("스타일 템플릿")); m2.addWidget(self.template)
        root.addLayout(m2)

        # 사용자 정의 스타일 상세 옵션
        m3 = QHBoxLayout()
        self.custom_title_size = QLineEdit("1.6em")
        self.custom_align = QComboBox(); self.custom_align.addItems(["left", "center", "right"])
        self.custom_weight = QComboBox(); self.custom_weight.addItems(["normal", "600", "bold"])
        self.custom_margin_top = QLineEdit("1.2em")
        self.custom_margin_bottom = QLineEdit("0.8em")
        m3.addWidget(QLabel("제목 크기")); m3.addWidget(self.custom_title_size)
        m3.addWidget(QLabel("제목 정렬")); m3.addWidget(self.custom_align)
        m3.addWidget(QLabel("제목 굵기")); m3.addWidget(self.custom_weight)
        m3.addWidget(QLabel("제목 상단여백")); m3.addWidget(self.custom_margin_top)
        m3.addWidget(QLabel("제목 하단여백")); m3.addWidget(self.custom_margin_bottom)
        root.addLayout(m3)

        m4 = QHBoxLayout()
        self.custom_body_size = QLineEdit("1em")
        self.custom_line_height = QLineEdit("1.8")
        self.custom_indent = QLineEdit("1em")
        self.custom_paragraph_margin_bottom = QLineEdit("0.8em")
        m4.addWidget(QLabel("본문 크기")); m4.addWidget(self.custom_body_size)
        m4.addWidget(QLabel("줄간격")); m4.addWidget(self.custom_line_height)
        m4.addWidget(QLabel("문단 들여쓰기")); m4.addWidget(self.custom_indent)
        m4.addWidget(QLabel("문단 하단여백")); m4.addWidget(self.custom_paragraph_margin_bottom)
        root.addLayout(m4)

        out = QHBoxLayout()
        self.output_dir = QLineEdit(); self.output_dir.setPlaceholderText("출력 폴더(선택)")
        out_pick = QPushButton("출력 폴더 선택")
        out.addWidget(self.output_dir); out.addWidget(out_pick)
        root.addLayout(out)

        cta = QHBoxLayout()
        convert = QPushButton("변환 실행")
        preview = QPushButton("CSS 미리보기")
        cta.addWidget(convert); cta.addWidget(preview); cta.addStretch(1)
        root.addLayout(cta)

        self.summary = QLabel("요약: 총 0건 / 성공 0건 / 실패 0건")
        root.addWidget(self.summary)

        self.log = QPlainTextEdit(); self.log.setReadOnly(True)
        root.addWidget(self.log)

        pick.clicked.connect(self.pick_files)
        out_pick.clicked.connect(self.pick_output_dir)
        convert.clicked.connect(self.convert)
        preview.clicked.connect(self.preview_css)
        self.drop.paths_dropped.connect(self.on_drop_paths)
        self.drop.message.connect(self.set_status)

    def pick_files(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(self, "TXT 파일 선택(여러 개 가능)", "", "Text Files (*.txt)")
        if paths:
            self.set_files(paths)

    def set_files(self, paths: list[str]) -> None:
        unique_paths = list(dict.fromkeys(paths))
        self.current_txt_paths = unique_paths
        display = "; ".join(unique_paths)
        self.file_path.setText(display)
        if unique_paths and not self.title.text().strip():
            self.title.setText(suggest_title_from_filename(unique_paths[0]))
        self.log.appendPlainText(f"입력 파일 {len(unique_paths)}개 설정")

    def pick_output_dir(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "출력 폴더 선택")
        if folder:
            self.output_dir.setText(folder)

    def on_drop_paths(self, paths: list[str]) -> None:
        txt = [p for p in paths if Path(p).suffix.lower() == ".txt"]
        ignored = len(paths) - len(txt)
        if not txt:
            self.set_status("TXT 파일만 허용됩니다.")
            return
        self.set_files(txt)
        self.set_status(f"TXT {len(txt)}개 추가, {ignored}개 무시")

    def _custom_opts(self) -> dict[str, Any]:
        return {
            "title_size": self.custom_title_size.text() or "1.6em",
            "title_align": self.custom_align.currentText(),
            "title_weight": self.custom_weight.currentText(),
            "title_margin_top": self.custom_margin_top.text() or "1.2em",
            "title_margin_bottom": self.custom_margin_bottom.text() or "0.8em",
            "body_size": self.custom_body_size.text() or "1em",
            "line_height": self.custom_line_height.text() or "1.8",
            "text_indent": self.custom_indent.text() or "1em",
            "paragraph_margin_bottom": self.custom_paragraph_margin_bottom.text() or "0.8em",
        }

    def preview_css(self) -> None:
        css = get_style_css(self.template.currentText(), self._custom_opts())
        self.log.appendPlainText("[CSS 미리보기]\n" + css)

    def convert(self) -> None:
        try:
            paths = self.current_txt_paths or [p.strip() for p in self.file_path.text().split(";") if p.strip()]
            if not paths:
                raise ValueError("TXT 파일을 선택하세요.")
            if self.split_mode.currentText() == "delimiter" and not self.delimiter.text():
                raise ValueError("delimiter 모드에서는 구분 문자열이 필요합니다.")

            success = 0
            failed = 0
            for path in paths:
                try:
                    text = read_text_file_with_fallback(path)
                    per_title = self.title.text().strip() if len(paths) == 1 and self.title.text().strip() else suggest_title_from_filename(path)
                    book = build_epub_from_text(
                        title=per_title,
                        author=self.author.text(),
                        language=self.language.text() or "ko",
                        text=text,
                        split_mode=self.split_mode.currentText(),
                        delimiter=self.delimiter.text(),
                        style_template=self.template.currentText(),
                        custom_style_options=self._custom_opts(),
                        source_filename=path,
                    )
                    output = make_output_epub_path(path, self.output_dir.text() or None, overwrite=False)
                    save_epub(book, output)
                    self.log.appendPlainText(f"성공: {path} -> {output}")
                    success += 1
                except Exception as each_exc:
                    self.log.appendPlainText(f"실패: {path} ({each_exc})")
                    failed += 1

            total = len(paths)
            self.summary.setText(f"요약: 총 {total}건 / 성공 {success}건 / 실패 {failed}건")
            if failed:
                self.set_status("EPUB 일부 실패")
                QMessageBox.warning(self, "변환 완료(일부 실패)", f"총 {total}건 중 성공 {success}건, 실패 {failed}건")
            else:
                self.set_status("EPUB 변환 성공")
        except Exception as exc:
            self.log.appendPlainText(f"실패: {exc}")
            QMessageBox.warning(self, "변환 실패", str(exc))
            self.set_status("EPUB 변환 실패")
