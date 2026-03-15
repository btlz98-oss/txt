from __future__ import annotations

from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit, QLabel, QPushButton
from services.counters import count_text_stats


class CounterTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QHBoxLayout(self)
        self.input = QPlainTextEdit()
        right = QVBoxLayout()
        self.labels = {k: QLabel() for k in ["chars_with_space","chars_without_space","line_count","line_count_non_empty","word_count","paragraph_count"]}
        right.addWidget(QLabel("기본 계산 방식 기준"))
        for k, v in self.labels.items():
            right.addWidget(v)
        sample = QPushButton("예시 불러오기")
        right.addWidget(sample); right.addStretch(1)
        root.addWidget(self.input, 3); root.addLayout(right, 2)
        self.input.textChanged.connect(self.refresh)
        sample.clicked.connect(lambda: self.input.setPlainText("안녕하세요 여러분\n\nTextCraft KR 테스트"))
        self.refresh()

    def refresh(self) -> None:
        s = count_text_stats(self.input.toPlainText())
        mapping = {
            "chars_with_space":"문자 수(공백 포함)","chars_without_space":"문자 수(공백 제외)",
            "line_count":"줄 수","line_count_non_empty":"빈 줄 제외 줄 수","word_count":"단어 수","paragraph_count":"문단 수"
        }
        for k, lbl in self.labels.items():
            lbl.setText(f"{mapping[k]}: {s[k]}")
        self.set_status("통계 갱신")
