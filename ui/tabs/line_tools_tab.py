from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QPlainTextEdit, QLabel,
    QCheckBox, QLineEdit, QComboBox
)

from services import line_tools


class LineToolsTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QVBoxLayout(self)
        self.input = QPlainTextEdit(); self.result = QPlainTextEdit()
        root.addWidget(QLabel("입력")); root.addWidget(self.input)

        row1 = QHBoxLayout()
        b_empty = QPushButton("빈 줄 제거")
        b_lb0 = QPushButton("줄바꿈 제거(붙임)")
        b_lb1 = QPushButton("줄바꿈 제거(공백)")
        self.delim = QLineEdit(); self.delim.setPlaceholderText("구분자")
        b_add = QPushButton("구분자 뒤 줄바꿈 추가")
        b_rm = QPushButton("구분자 주변 줄바꿈 제거")
        for w in [b_empty,b_lb0,b_lb1,self.delim,b_add,b_rm]: row1.addWidget(w)
        root.addLayout(row1)

        row2 = QHBoxLayout()
        self.sort_mode = QComboBox(); self.sort_mode.addItems(["문자열 오름차순","문자열 내림차순","숫자 오름차순","숫자 내림차순"])
        self.ignore_case = QCheckBox("대소문자 무시"); self.ignore_case.setChecked(True)
        self.strip_sort = QCheckBox("앞뒤 공백 무시"); self.strip_sort.setChecked(True)
        b_sort = QPushButton("줄 정렬")
        self.unique_mode = QComboBox(); self.unique_mode.addItems(["preserve order","sorted unique"])
        self.case_sensitive = QCheckBox("중복 제거 시 대소문자 구분"); self.case_sensitive.setChecked(True)
        self.ignore_blank = QCheckBox("중복 제거 시 빈 줄 제외")
        b_unique = QPushButton("중복 줄 제거")
        for w in [self.sort_mode,self.ignore_case,self.strip_sort,b_sort,self.unique_mode,self.case_sensitive,self.ignore_blank,b_unique]: row2.addWidget(w)
        root.addLayout(row2)

        root.addWidget(QLabel("결과")); root.addWidget(self.result)
        row3 = QHBoxLayout()
        sample = QPushButton("예시 불러오기"); copy = QPushButton("결과 복사")
        row3.addWidget(sample); row3.addWidget(copy); row3.addStretch(1); root.addLayout(row3)

        b_empty.clicked.connect(lambda: self._set(line_tools.remove_empty_lines(self.input.toPlainText())))
        b_lb0.clicked.connect(lambda: self._set(line_tools.remove_linebreaks(self.input.toPlainText(), False)))
        b_lb1.clicked.connect(lambda: self._set(line_tools.remove_linebreaks(self.input.toPlainText(), True)))
        b_add.clicked.connect(lambda: self._set(line_tools.add_linebreak_by_delimiter(self.input.toPlainText(), self.delim.text())))
        b_rm.clicked.connect(lambda: self._set(line_tools.remove_linebreak_near_delimiter(self.input.toPlainText(), self.delim.text())))
        b_sort.clicked.connect(self.on_sort)
        b_unique.clicked.connect(self.on_unique)
        sample.clicked.connect(lambda: self.input.setPlainText("10\n2\napple\nBanana\napple\n"))
        copy.clicked.connect(lambda: self.result.copy())

    def _set(self, text: str) -> None:
        self.result.setPlainText(text)
        self.set_status("줄 도구 실행 완료")

    def on_sort(self) -> None:
        mode = self.sort_mode.currentText()
        self._set(line_tools.sort_lines(
            self.input.toPlainText(),
            reverse="내림" in mode,
            numeric="숫자" in mode,
            ignore_case=self.ignore_case.isChecked(),
            strip_for_sort=self.strip_sort.isChecked(),
        ))

    def on_unique(self) -> None:
        self._set(line_tools.unique_lines(
            self.input.toPlainText(),
            preserve_order=self.unique_mode.currentText() == "preserve order",
            ignore_blank=self.ignore_blank.isChecked(),
            case_sensitive=self.case_sensitive.isChecked(),
        ))
