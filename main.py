from __future__ import annotations

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main() -> int:
    """TextCraft KR 실행 진입점."""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
