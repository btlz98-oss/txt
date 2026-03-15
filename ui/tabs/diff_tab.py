from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QLabel, QComboBox, QPushButton, QTextBrowser
from services.diff_tools import diff_by_line, diff_by_word, diff_by_char


class DiffTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QVBoxLayout(self)
        row = QHBoxLayout()
        self.a = QPlainTextEdit(); self.b = QPlainTextEdit()
        self.a.setPlaceholderText("원문"); self.b.setPlaceholderText("비교문")
        row.addWidget(self.a); row.addWidget(self.b)
        root.addLayout(row)
        ctrl = QHBoxLayout()
        self.mode = QComboBox(); self.mode.addItems(["줄 단위", "단어 단위", "문자 단위"])
        run = QPushButton("비교 실행"); sample = QPushButton("예시 불러오기")
        ctrl.addWidget(QLabel("비교 단위")); ctrl.addWidget(self.mode); ctrl.addWidget(run); ctrl.addWidget(sample); ctrl.addStretch(1)
        root.addLayout(ctrl)
        self.result = QTextBrowser(); root.addWidget(self.result)
        run.clicked.connect(self.on_run)
        sample.clicked.connect(lambda: (self.a.setPlainText("안녕 세상"), self.b.setPlainText("안녕 새로운 세상")))

    def on_run(self) -> None:
        m = self.mode.currentText()
        if m == "줄 단위":
            html = diff_by_line(self.a.toPlainText(), self.b.toPlainText())
        elif m == "단어 단위":
            html = diff_by_word(self.a.toPlainText(), self.b.toPlainText())
        else:
            html = diff_by_char(self.a.toPlainText(), self.b.toPlainText())
        self.result.setHtml(html)
        self.set_status("Diff 완료")
