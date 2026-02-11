from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from stress_wizard.config import load_settings
from stress_wizard.logging_utils import setup_logging
from stress_wizard.ui.dark_theme import DARK_STYLESHEET
from stress_wizard.ui.main_window import MainWindow


def run() -> int:
    setup_logging()
    settings = load_settings()

    app = QApplication(sys.argv)
    app.setApplicationName("Stress Scenario Generation Wizard")
    app.setStyleSheet(DARK_STYLESHEET)

    window = MainWindow(settings)
    window.show()

    return app.exec()
