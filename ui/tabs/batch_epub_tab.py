from __future__ import annotations

from pathlib import Path
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QFileDialog, QCheckBox,
    QLineEdit, QLabel, QProgressBar, QTableWidget, QTableWidgetItem, QComboBox
)

from services.batch_tools import collect_txt_files_from_paths, batch_convert_txt_to_epub
from services.style_templates import get_style_template_names
from ui.widgets import DropArea


class BatchEpubTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QVBoxLayout(self)

        buttons = QHBoxLayout()
        add_files = QPushButton("파일 추가")
        add_folder = QPushButton("폴더 추가")
        remove_sel = QPushButton("선택 제거")
        clear_all = QPushButton("목록 비우기")
        for b in [add_files, add_folder, remove_sel, clear_all]:
            buttons.addWidget(b)
        buttons.addStretch(1)
        root.addLayout(buttons)

        self.list = QListWidget(); root.addWidget(self.list)
        self.drop = DropArea("파일/폴더 드롭 (txt 자동 필터링)"); root.addWidget(self.drop)

        opts1 = QHBoxLayout()
        self.recursive = QCheckBox("하위 폴더 포함")
        self.overwrite = QCheckBox("기존 epub 덮어쓰기")
        self.retry_failed = QCheckBox("실패 파일만 다시 시도")
        self.output_dir = QLineEdit(); self.output_dir.setPlaceholderText("출력 폴더")
        out_btn = QPushButton("출력 폴더 선택")
        for w in [self.recursive, self.overwrite, self.retry_failed, QLabel("출력"), self.output_dir, out_btn]:
            opts1.addWidget(w)
        root.addLayout(opts1)

        opts2 = QHBoxLayout()
        self.prefix = QLineEdit(); self.suffix = QLineEdit(); self.author = QLineEdit(); self.language = QLineEdit("ko")
        self.template = QComboBox(); self.template.addItems(get_style_template_names())
        self.split_mode = QComboBox(); self.split_mode.addItems(["single", "blankline", "delimiter"])
        self.delimiter = QLineEdit()
        for lbl, w in [
            ("제목 접두", self.prefix), ("제목 접미", self.suffix), ("공통 저자", self.author),
            ("공통 언어", self.language), ("템플릿", self.template), ("분리", self.split_mode), ("구분자", self.delimiter)
        ]:
            opts2.addWidget(QLabel(lbl)); opts2.addWidget(w)
        root.addLayout(opts2)

        # 배치 사용자 정의 스타일
        opts3 = QHBoxLayout()
        self.custom_title_size = QLineEdit("1.6em")
        self.custom_align = QComboBox(); self.custom_align.addItems(["left", "center", "right"])
        self.custom_weight = QComboBox(); self.custom_weight.addItems(["normal", "600", "bold"])
        self.custom_margin_top = QLineEdit("1.2em")
        self.custom_margin_bottom = QLineEdit("0.8em")
        for lbl, w in [
            ("제목 크기", self.custom_title_size), ("제목 정렬", self.custom_align), ("제목 굵기", self.custom_weight),
            ("제목 상단여백", self.custom_margin_top), ("제목 하단여백", self.custom_margin_bottom)
        ]:
            opts3.addWidget(QLabel(lbl)); opts3.addWidget(w)
        root.addLayout(opts3)

        opts4 = QHBoxLayout()
        self.custom_body_size = QLineEdit("1em")
        self.custom_line_height = QLineEdit("1.8")
        self.custom_indent = QLineEdit("1em")
        self.custom_paragraph_margin_bottom = QLineEdit("0.8em")
        for lbl, w in [
            ("본문 크기", self.custom_body_size), ("줄간격", self.custom_line_height),
            ("문단 들여쓰기", self.custom_indent), ("문단 하단여백", self.custom_paragraph_margin_bottom)
        ]:
            opts4.addWidget(QLabel(lbl)); opts4.addWidget(w)
        root.addLayout(opts4)

        run = QPushButton("일괄 변환 실행")
        self.progress = QProgressBar(); self.progress.setValue(0)
        root.addWidget(run); root.addWidget(self.progress)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["원본 파일명", "출력 epub 파일명", "상태", "메시지"])
        root.addWidget(self.table)

        add_files.clicked.connect(self.on_add_files)
        add_folder.clicked.connect(self.on_add_folder)
        remove_sel.clicked.connect(self.on_remove_selected)
        clear_all.clicked.connect(self.list.clear)
        out_btn.clicked.connect(self.on_pick_output)
        run.clicked.connect(self.on_run)
        self.drop.paths_dropped.connect(self.on_drop)
        self.drop.message.connect(self.set_status)

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

    def _add_paths(self, paths: list[str]) -> tuple[int, int]:
        txts = collect_txt_files_from_paths(paths, recursive=self.recursive.isChecked())
        existing = {self.list.item(i).text() for i in range(self.list.count())}
        added = 0
        for p in txts:
            if str(p) not in existing:
                self.list.addItem(str(p))
                added += 1
        ignored = max(0, len(paths) - len(txts))
        return added, ignored

    def on_add_files(self) -> None:
        files, _ = QFileDialog.getOpenFileNames(self, "TXT 파일 추가", "", "Text Files (*.txt)")
        added, ignored = self._add_paths(files)
        self.set_status(f"파일 추가: {added}개 추가, {ignored}개 무시")

    def on_add_folder(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "폴더 추가")
        if folder:
            added, ignored = self._add_paths([folder])
            self.set_status(f"폴더 추가: {added}개 추가, {ignored}개 무시")

    def on_drop(self, paths: list[str]) -> None:
        if not paths:
            self.set_status("드롭된 항목이 없습니다.")
            return
        added, ignored = self._add_paths(paths)
        self.set_status(f"드롭 처리: {added}개 추가, {ignored}개 무시")

    def on_remove_selected(self) -> None:
        for item in self.list.selectedItems():
            self.list.takeItem(self.list.row(item))

    def on_pick_output(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, "출력 폴더 선택")
        if folder:
            self.output_dir.setText(folder)

    def _collect_retry_paths(self) -> list[str]:
        retry_paths: list[str] = []
        for r in range(self.table.rowCount()):
            status_item = self.table.item(r, 2)
            input_item = self.table.item(r, 0)
            if not status_item or not input_item:
                continue
            if status_item.text() == "실패":
                original_path = input_item.data(Qt.UserRole)
                if isinstance(original_path, str) and original_path:
                    retry_paths.append(original_path)
        return retry_paths

    def on_run(self) -> None:
        paths = [self.list.item(i).text() for i in range(self.list.count())]
        if self.retry_failed.isChecked() and self.table.rowCount() > 0:
            paths = self._collect_retry_paths()

        results = batch_convert_txt_to_epub(
            paths=paths,
            output_dir=self.output_dir.text() or None,
            recursive=self.recursive.isChecked(),
            overwrite=self.overwrite.isChecked(),
            common_author=self.author.text(),
            common_language=self.language.text() or "ko",
            title_prefix=self.prefix.text(),
            title_suffix=self.suffix.text(),
            split_mode=self.split_mode.currentText(),
            delimiter=self.delimiter.text() or None,
            style_template=self.template.currentText(),
            custom_style_options=self._custom_opts() if self.template.currentText() == "사용자 정의형" else None,
        )

        self.table.setRowCount(0)
        total = max(1, len(results))
        for idx, row in enumerate(results, 1):
            r = self.table.rowCount()
            self.table.insertRow(r)
            input_item = QTableWidgetItem(Path(row["input"]).name)
            input_item.setData(Qt.UserRole, row["input"])  # 원본 절대경로 보존
            self.table.setItem(r, 0, input_item)
            self.table.setItem(r, 1, QTableWidgetItem(Path(row["output"]).name if row["output"] else ""))
            self.table.setItem(r, 2, QTableWidgetItem(row["status"]))
            self.table.setItem(r, 3, QTableWidgetItem(row["message"]))
            self.progress.setValue(int(idx / total * 100))
        self.set_status(f"일괄 변환 완료: {len(results)}개")
