from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from stress_wizard.config import AppSettings
from stress_wizard.ui.widgets.pandas_model import LazyDataFrameModel


class ScenarioLibraryWidget(QWidget):
    def __init__(self, settings: AppSettings, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.model = LazyDataFrameModel(pd.DataFrame())
        self._build_ui()
        self.refresh()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        row = QHBoxLayout()
        refresh_btn = QPushButton("Refresh Library")
        refresh_btn.clicked.connect(self.refresh)
        compare_btn = QPushButton("Compare Selected (2)")
        compare_btn.clicked.connect(self.compare_selected)
        row.addWidget(refresh_btn)
        row.addWidget(compare_btn)
        row.addStretch(1)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.table.setAlternatingRowColors(True)

        self.compare_text = QTextEdit()
        self.compare_text.setReadOnly(True)
        self.compare_text.setMinimumHeight(140)

        root.addLayout(row)
        root.addWidget(QLabel("Saved Scenarios"))
        root.addWidget(self.table, stretch=1)
        root.addWidget(QLabel("Compare Output"))
        root.addWidget(self.compare_text)

    def refresh(self) -> None:
        root = Path(self.settings.root_path) / "scenarios"
        rows = []
        if root.exists():
            for folder in sorted(root.glob("*")):
                cfg = folder / "scenario_config.json"
                if not cfg.exists():
                    continue
                try:
                    payload = json.loads(cfg.read_text(encoding="utf-8"))
                    meta = payload.get("metadata", {})
                    rows.append(
                        {
                            "folder": folder.name,
                            "scenario_id": meta.get("scenario_id"),
                            "name": meta.get("name"),
                            "severity": meta.get("severity"),
                            "author": meta.get("author"),
                            "created_at": meta.get("created_at"),
                            "horizon_days": meta.get("horizon_days"),
                        }
                    )
                except Exception:
                    continue
        self.model.set_frame(pd.DataFrame(rows))

    def compare_selected(self) -> None:
        selected = sorted({ix.row() for ix in self.table.selectionModel().selectedRows()})
        frame = self.model.frame.reset_index(drop=True)
        if len(selected) < 2:
            self.compare_text.setPlainText("Select at least two scenarios to compare.")
            return

        i, j = selected[:2]
        a = frame.loc[i].to_dict()
        b = frame.loc[j].to_dict()

        lines = [
            f"Scenario A: {a.get('name')} ({a.get('severity')})",
            f"Scenario B: {b.get('name')} ({b.get('severity')})",
            "",
            "Differences:",
        ]
        for key in ["severity", "horizon_days", "author", "created_at"]:
            if str(a.get(key)) != str(b.get(key)):
                lines.append(f"- {key}: {a.get(key)} vs {b.get(key)}")

        if len(lines) == 4:
            lines.append("- No metadata differences found across selected dimensions.")

        self.compare_text.setPlainText("\n".join(lines))
