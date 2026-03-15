from __future__ import annotations

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QComboBox,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QLabel,
)

from services.cleaners import apply_cleanup_pipeline
from ui.widgets import common_io_buttons


class CleanupTab(QWidget):
    def __init__(self, set_status):
        super().__init__()
        self.set_status = set_status
        root = QHBoxLayout(self)

        left = QVBoxLayout()
        self.cb_bracket = QCheckBox("괄호 및 내용 제거")
        self.cb_eng = QCheckBox("영문 제거")
        self.cb_hanja = QCheckBox("한자 제거")
        self.cb_special = QCheckBox("특수문자 제거")
        self.mode = QComboBox(); self.mode.addItems(["basic", "strict", "custom_punctuation"])
        self.allowed = QLineEdit(); self.allowed.setPlaceholderText("custom 모드 허용 문장부호")
        self.cb_merge = QCheckBox("문장 내 줄바꿈 합치기")
        self.cb_collapse = QCheckBox("문단 사이 빈 줄 제거")
        self.cb_trim = QCheckBox("앞뒤 공백 정리")
        self.cb_norm = QCheckBox("연속 공백 정리")
        run = QPushButton("실행")
        for w in [self.cb_bracket, self.cb_eng, self.cb_hanja, self.cb_special, QLabel("특수문자 모드"), self.mode, self.allowed, self.cb_merge, self.cb_collapse, self.cb_trim, self.cb_norm, run]:
            left.addWidget(w)
        left.addStretch(1)

        right = QVBoxLayout()
        self.input = QPlainTextEdit(); self.result = QPlainTextEdit()
        self.input.setPlaceholderText("입력")
        self.result.setPlaceholderText("결과")
        right.addWidget(QLabel("입력")); right.addWidget(self.input)
        right.addWidget(QLabel("결과")); right.addWidget(self.result)
        row, btns = common_io_buttons(); right.addLayout(row)

        root.addLayout(left, 1); root.addLayout(right, 3)

        run.clicked.connect(self.on_run)
        btns["예시 불러오기"].clicked.connect(lambda: self.input.setPlainText("안녕하세요(테스트)\n\n漢字 ABC !!!"))
        btns["클립보드 붙여넣기"].clicked.connect(self.paste_from_clipboard)
        btns["결과를 입력창으로 복사"].clicked.connect(self.copy_result_to_input)
        btns["입력 비우기"].clicked.connect(self.input.clear)
        btns["결과 비우기"].clicked.connect(self.result.clear)
        btns["결과 복사"].clicked.connect(lambda: self.result.copy())

    def paste_from_clipboard(self) -> None:
        clip_text = QApplication.clipboard().text()
        if clip_text:
            self.input.setPlainText(clip_text)
            self.set_status("클립보드 내용을 입력창에 붙여넣었습니다.")
        else:
            self.set_status("클립보드에 텍스트가 없습니다.")

    def copy_result_to_input(self) -> None:
        self.input.setPlainText(self.result.toPlainText())
        self.set_status("결과를 입력창으로 복사했습니다.")

    def on_run(self) -> None:
        opts = {
            "remove_brackets": self.cb_bracket.isChecked(), "remove_english": self.cb_eng.isChecked(),
            "remove_hanja": self.cb_hanja.isChecked(), "remove_special": self.cb_special.isChecked(),
            "special_mode": self.mode.currentText(), "allowed_punctuation": self.allowed.text(),
            "merge_intraline_breaks": self.cb_merge.isChecked(), "collapse_blank_lines": self.cb_collapse.isChecked(),
            "trim_lines": self.cb_trim.isChecked(), "normalize_spaces": self.cb_norm.isChecked(),
        }
        self.result.setPlainText(apply_cleanup_pipeline(self.input.toPlainText(), opts))
        self.set_status("문단 정리 완료")
