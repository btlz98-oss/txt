from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QPushButton, QHBoxLayout


class DropArea(QFrame):
    """파일/폴더 드롭 공통 위젯."""

    paths_dropped = Signal(list)
    message = Signal(str)

    def __init__(self, text: str = "여기에 파일/폴더를 드롭하세요") -> None:
        super().__init__()
        self.setAcceptDrops(True)
        self.setFrameShape(QFrame.StyledPanel)
        self.label = QLabel(text)
        self.label.setStyleSheet("color:#555;")
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setStyleSheet("QFrame{border:2px dashed #999; border-radius:8px; padding:12px;}")

    def dragEnterEvent(self, event):  # noqa: N802
        if event.mimeData().hasUrls():
            self.setStyleSheet("QFrame{border:2px dashed #2a9d8f; background:#ecfffb; border-radius:8px; padding:12px;}")
            event.acceptProposedAction()

    def dragLeaveEvent(self, event):  # noqa: N802
        self.setStyleSheet("QFrame{border:2px dashed #999; border-radius:8px; padding:12px;}")
        event.accept()

    def dropEvent(self, event):  # noqa: N802
        self.setStyleSheet("QFrame{border:2px dashed #999; border-radius:8px; padding:12px;}")
        urls = event.mimeData().urls()
        paths = [Path(u.toLocalFile()) for u in urls if u.isLocalFile()]
        if not paths:
            self.message.emit("드롭된 경로가 없습니다.")
            return
        self.paths_dropped.emit([str(p) for p in paths])
        self.message.emit(f"{len(paths)}개 경로 드롭됨")
        event.acceptProposedAction()


def common_io_buttons() -> tuple[QHBoxLayout, dict[str, QPushButton]]:
    row = QHBoxLayout()
    labels = [
        "예시 불러오기",
        "클립보드 붙여넣기",
        "결과를 입력창으로 복사",
        "입력 비우기",
        "결과 비우기",
        "결과 복사",
    ]
    btns: dict[str, QPushButton] = {}
    for lbl in labels:
        b = QPushButton(lbl)
        row.addWidget(b)
        btns[lbl] = b
    row.addStretch(1)
    return row, btns
