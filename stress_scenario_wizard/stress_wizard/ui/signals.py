from __future__ import annotations

from PySide6.QtCore import QObject, Signal


class AppSignals(QObject):
    data_changed = Signal()
    scenario_changed = Signal()
    calculation_complete = Signal()
    governance_changed = Signal()
    status_message = Signal(str)
