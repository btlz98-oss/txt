from __future__ import annotations

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QLabel
from services.encoders import html_escape_text, html_unescape_text, url_encode_text, url_decode_text


class EncoderTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QVBoxLayout(self)
        self.input = QPlainTextEdit(); self.result = QPlainTextEdit()
        root.addWidget(QLabel("입력")); root.addWidget(self.input)
        row = QHBoxLayout()
        b1 = QPushButton("HTML Escape")
        b2 = QPushButton("HTML Unescape")
        b3 = QPushButton("URL Encode")
        b4 = QPushButton("URL Decode")
        sample = QPushButton("예시 불러오기")
        for b in [b1,b2,b3,b4,sample]: row.addWidget(b)
        root.addLayout(row)
        root.addWidget(QLabel("결과")); root.addWidget(self.result)
        b1.clicked.connect(lambda: self._set(html_escape_text(self.input.toPlainText())))
        b2.clicked.connect(lambda: self._set(html_unescape_text(self.input.toPlainText())))
        b3.clicked.connect(lambda: self._set(url_encode_text(self.input.toPlainText())))
        b4.clicked.connect(lambda: self._set(url_decode_text(self.input.toPlainText())))
        sample.clicked.connect(lambda: self.input.setPlainText("<a>한글 테스트</a> hello world"))

    def _set(self, t: str) -> None:
        self.result.setPlainText(t)
        self.set_status("인코딩/디코딩 완료")
