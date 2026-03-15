from __future__ import annotations

from PySide6.QtWidgets import QMainWindow, QTabWidget, QLabel

from ui.tabs.cleanup_tab import CleanupTab
from ui.tabs.line_tools_tab import LineToolsTab
from ui.tabs.counter_tab import CounterTab
from ui.tabs.diff_tab import DiffTab
from ui.tabs.encoder_tab import EncoderTab
from ui.tabs.epub_tab import EpubTab
from ui.tabs.batch_epub_tab import BatchEpubTab


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("TextCraft KR")
        self.resize(1300, 850)
        self.status = QLabel("준비")
        self.statusBar().addWidget(self.status)

        tabs = QTabWidget()
        tabs.addTab(CleanupTab(self.set_status), "문단 정리기")
        tabs.addTab(LineToolsTab(self.set_status), "줄 도구")
        tabs.addTab(CounterTab(self.set_status), "문자/단어/줄 수")
        tabs.addTab(DiffTab(self.set_status), "텍스트 비교")
        tabs.addTab(EncoderTab(self.set_status), "HTML/URL 인코딩")
        tabs.addTab(EpubTab(self.set_status), "TXT → EPUB")
        tabs.addTab(BatchEpubTab(self.set_status), "EPUB 일괄 변환기")
        self.setCentralWidget(tabs)

    def set_status(self, text: str) -> None:
        self.status.setText(text)
