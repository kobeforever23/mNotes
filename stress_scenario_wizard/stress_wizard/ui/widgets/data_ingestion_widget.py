from __future__ import annotations

from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QSplitter,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from stress_wizard.app_state import AppState
from stress_wizard.ingestion.column_mapper import REQUIRED_FIELDS, suggest_mappings
from stress_wizard.ingestion.file_import import FileImporter
from stress_wizard.ingestion.validator import validate_bundle
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.pandas_model import LazyDataFrameModel


class DataIngestionWidget(QWidget):
    def __init__(self, state: AppState, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.signals = signals
        self.file_importer = FileImporter()

        self.preview_model = LazyDataFrameModel(pd.DataFrame())
        self.stats_model = LazyDataFrameModel(pd.DataFrame())
        self.mapping_model = LazyDataFrameModel(pd.DataFrame())

        self._build_ui()
        self._load_bundle_preview()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        source_group = QGroupBox("Data Source Setup")
        source_layout = QFormLayout(source_group)

        self.source_combo = QComboBox()
        self.source_combo.addItems(["File Import", "SQL Server"])
        source_layout.addRow("Source", self.source_combo)

        file_row = QHBoxLayout()
        self.file_path = QLineEdit()
        self.file_path.setPlaceholderText("Select CSV/XLSX/JSON/Parquet")
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self._browse_file)
        self.sheet_combo = QComboBox()
        self.sheet_combo.setEnabled(False)
        self.sheet_combo.setMinimumWidth(120)
        file_row.addWidget(self.file_path, stretch=1)
        file_row.addWidget(self.sheet_combo)
        file_row.addWidget(browse_btn)
        source_layout.addRow("File", file_row)

        self.category_combo = QComboBox()
        self.category_combo.addItems(["positions", "sensitivities", "market_data", "risk_drivers"])
        source_layout.addRow("Target Category", self.category_combo)

        load_row = QHBoxLayout()
        self.load_btn = QPushButton("Load Into Bundle")
        self.load_btn.clicked.connect(self._load_file)
        validate_btn = QPushButton("Run Validation")
        validate_btn.clicked.connect(self._run_validation)
        load_row.addWidget(self.load_btn)
        load_row.addWidget(validate_btn)
        source_layout.addRow("Actions", load_row)

        sql_help = QLabel("SQL connection profiles are supported in the backend module; demo mode uses file import and synthetic data.")
        sql_help.setWordWrap(True)
        source_layout.addRow("SQL", sql_help)

        generator_group = QGroupBox("Synthetic Scale Generator")
        gen_layout = QHBoxLayout(generator_group)
        self.risk_driver_count = QSpinBox()
        self.risk_driver_count.setRange(10_000, 400_000)
        self.risk_driver_count.setSingleStep(10_000)
        self.risk_driver_count.setValue(60_000)
        regen_btn = QPushButton("Regenerate Demo Dataset")
        regen_btn.clicked.connect(self._regenerate_bundle)
        gen_layout.addWidget(QLabel("Risk Drivers:"))
        gen_layout.addWidget(self.risk_driver_count)
        gen_layout.addWidget(regen_btn)
        gen_layout.addStretch(1)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Preview (first 100 rows)"))
        preview_table = QTableView()
        preview_table.setModel(self.preview_model)
        preview_table.setAlternatingRowColors(True)
        preview_table.setSortingEnabled(True)
        left_layout.addWidget(preview_table)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Column Stats"))
        stats_table = QTableView()
        stats_table.setModel(self.stats_model)
        stats_table.setAlternatingRowColors(True)
        right_layout.addWidget(stats_table)

        right_layout.addWidget(QLabel("Auto-Mapping Suggestions"))
        mapping_table = QTableView()
        mapping_table.setModel(self.mapping_model)
        mapping_table.setAlternatingRowColors(True)
        right_layout.addWidget(mapping_table)

        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setSizes([700, 600])

        self.validation_text = QTextEdit()
        self.validation_text.setReadOnly(True)
        self.validation_text.setMinimumHeight(140)

        root.addWidget(source_group)
        root.addWidget(generator_group)
        root.addWidget(splitter, stretch=1)
        root.addWidget(QLabel("Data Validation Dashboard"))
        root.addWidget(self.validation_text)

    def _browse_file(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Data File",
            str(Path.cwd()),
            "Data Files (*.csv *.xlsx *.xls *.json *.parquet)",
        )
        if not file_path:
            return
        self.file_path.setText(file_path)
        self._refresh_sheet_options(file_path)

    def _refresh_sheet_options(self, file_path: str) -> None:
        sheets = self.file_importer.available_sheets(file_path)
        self.sheet_combo.clear()
        if sheets:
            self.sheet_combo.addItems(sheets)
            self.sheet_combo.setEnabled(True)
        else:
            self.sheet_combo.setEnabled(False)

    def _load_file(self) -> None:
        path = self.file_path.text().strip()
        if not path:
            QMessageBox.warning(self, "File Missing", "Select a file to import.")
            return

        try:
            sheet = self.sheet_combo.currentText() if self.sheet_combo.isEnabled() else None
            frame = self.file_importer.load(path, sheet_name=sheet)
            category = self.category_combo.currentText()
            setattr(self.state.data_bundle, category, frame)
            self.signals.data_changed.emit()
            self.signals.status_message.emit(f"Loaded {len(frame):,} rows into {category}.")
            self._preview_frame(frame, category)
        except Exception as exc:
            QMessageBox.critical(self, "Import Failed", str(exc))

    def _preview_frame(self, frame: pd.DataFrame, category: str) -> None:
        preview = self.file_importer.preview(frame)
        stats = self.file_importer.column_stats(frame)
        mappings = suggest_mappings(frame.columns.tolist(), category)

        mapping_df = pd.DataFrame(
            [
                {
                    "source": m.source,
                    "target": m.target,
                    "confidence": m.confidence,
                    "reason": m.reason,
                }
                for m in mappings
            ]
        )

        self.preview_model.set_frame(preview)
        self.stats_model.set_frame(stats)
        self.mapping_model.set_frame(mapping_df)

    def _load_bundle_preview(self) -> None:
        category = self.category_combo.currentText()
        frame = getattr(self.state.data_bundle, category)
        self._preview_frame(frame, category)

    def _run_validation(self) -> None:
        bundle = self.state.data_bundle
        scorecard = validate_bundle(
            positions=bundle.positions,
            sensitivities=bundle.sensitivities,
            market_data=bundle.market_data,
            risk_drivers=bundle.risk_drivers,
        )

        lines = [
            f"Overall Data Quality Score: {scorecard.total_score:.2f}",
            f"Positions with complete Greeks: {scorecard.coverage_positions_with_complete_greeks:.2f}%",
            f"Risk drivers with market coverage: {scorecard.coverage_risk_drivers_with_market_data:.2f}%",
            f"Duplicates detected: {scorecard.duplicate_count}",
            f"Stale market rows (older than T-1): {scorecard.stale_market_data_count}",
            "",
            "Missing Required Columns:",
        ]

        for category, missing in scorecard.missing_required_columns.items():
            val = ", ".join(missing) if missing else "None"
            lines.append(f"- {category}: {val}")

        lines.append("")
        lines.append("Issues:")
        if scorecard.issues:
            for issue in scorecard.issues:
                lines.append(f"[{issue.severity}] {issue.category}: {issue.message}")
                lines.append(f"  Recommendation: {issue.recommendation}")
        else:
            lines.append("No data quality issues detected.")

        self.validation_text.setPlainText("\n".join(lines))

    def _regenerate_bundle(self) -> None:
        count = int(self.risk_driver_count.value())
        self.state.regenerate_risk_drivers(count)
        self.signals.data_changed.emit()
        self.signals.status_message.emit(f"Generated demo bundle with {count:,} risk drivers.")
        self._load_bundle_preview()
