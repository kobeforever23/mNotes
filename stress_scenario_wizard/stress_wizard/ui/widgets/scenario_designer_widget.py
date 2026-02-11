from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSlider,
    QSpinBox,
    QDoubleSpinBox,
    QSplitter,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from stress_wizard.app_state import AppState
from stress_wizard.ingestion.file_import import FileImporter
from stress_wizard.scenario.bottom_up import apply_bulk_shock, search_risk_drivers
from stress_wizard.scenario.reconciliation import blend_shocks
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.pandas_model import LazyDataFrameModel


class ScenarioDesignerWidget(QWidget):
    def __init__(self, state: AppState, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.signals = signals
        self.file_importer = FileImporter()

        self.asset_shock_model = LazyDataFrameModel(pd.DataFrame())
        self.driver_model = LazyDataFrameModel(pd.DataFrame())

        self._build_ui()
        self._initialize_defaults()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        top_group = QGroupBox("Top-Down Scenario Builder")
        top_layout = QVBoxLayout(top_group)

        name_layout = QHBoxLayout()
        self.scenario_name = QLineEdit()
        self.scenario_name.setPlaceholderText("Scenario name")
        self.approach_combo = QComboBox()
        self.approach_combo.addItems(["Top-Down", "Bottom-Up", "Hybrid"])
        name_layout.addWidget(QLabel("Name"))
        name_layout.addWidget(self.scenario_name, stretch=1)
        name_layout.addWidget(QLabel("Approach"))
        name_layout.addWidget(self.approach_combo)

        self.narrative = QTextEdit()
        self.narrative.setPlaceholderText("Write or paste macro narrative.")
        self.narrative.setMinimumHeight(80)

        theme_grid = QGridLayout()
        self.theme_inputs: dict[str, QDoubleSpinBox] = {}
        for idx, theme in enumerate(["Recession", "Stagflation", "Rate Shock", "Credit Crisis", "Geopolitical", "Liquidity Squeeze"]):
            spin = QDoubleSpinBox()
            spin.setRange(0.0, 1.0)
            spin.setSingleStep(0.05)
            spin.setValue(0.1)
            self.theme_inputs[theme] = spin
            row, col = divmod(idx, 3)
            theme_grid.addWidget(QLabel(theme), row * 2, col)
            theme_grid.addWidget(spin, row * 2 + 1, col)

        control_form = QFormLayout()
        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["Moderate", "Severe", "Extreme", "Custom"])
        self.severity_scale = QDoubleSpinBox()
        self.severity_scale.setRange(0.1, 6.0)
        self.severity_scale.setValue(1.0)
        self.severity_scale.setSingleStep(0.1)

        self.horizon_days = QSpinBox()
        self.horizon_days.setRange(1, 365)
        self.horizon_days.setValue(10)

        self.calibration_combo = QComboBox()
        self.calibration_combo.addItems(["Historical", "Statistical", "Hypothetical", "Hybrid"])

        self.template_combo = QComboBox()
        self.template_combo.addItems(["Rate Hike", "Credit Crunch"])

        control_form.addRow("Severity Tier", self.severity_combo)
        control_form.addRow("Severity Scale", self.severity_scale)
        control_form.addRow("Horizon (Days)", self.horizon_days)
        control_form.addRow("Calibration", self.calibration_combo)
        control_form.addRow("Transmission Template", self.template_combo)

        action_row = QHBoxLayout()
        apply_btn = QPushButton("Apply Top-Down Configuration")
        apply_btn.clicked.connect(self._apply_top_down)
        ai_btn = QPushButton("AI Narrative (Template)")
        ai_btn.clicked.connect(self._mock_ai_narrative)
        action_row.addWidget(apply_btn)
        action_row.addWidget(ai_btn)

        self.coherence_box = QTextEdit()
        self.coherence_box.setReadOnly(True)
        self.coherence_box.setMinimumHeight(70)

        top_layout.addLayout(name_layout)
        top_layout.addWidget(QLabel("Narrative & Macro Theme"))
        top_layout.addWidget(self.narrative)
        top_layout.addLayout(theme_grid)
        top_layout.addLayout(control_form)
        top_layout.addLayout(action_row)
        top_layout.addWidget(QLabel("Coherence Checker"))
        top_layout.addWidget(self.coherence_box)

        shock_group = QGroupBox("Asset Class Shock Grid (Editable via Top-Down Controls)")
        shock_layout = QVBoxLayout(shock_group)
        shock_table = QTableView()
        shock_table.setModel(self.asset_shock_model)
        shock_table.setAlternatingRowColors(True)
        shock_layout.addWidget(shock_table)

        bottom_group = QGroupBox("Bottom-Up Driver Builder")
        bottom_layout = QVBoxLayout(bottom_group)

        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search 300k+ drivers by id/name/asset class/geography/tenor")
        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self._search_drivers)
        import_btn = QPushButton("Import Driver Shocks")
        import_btn.clicked.connect(self._import_driver_shocks)
        search_row.addWidget(self.search_input, stretch=1)
        search_row.addWidget(search_btn)
        search_row.addWidget(import_btn)

        driver_table = QTableView()
        driver_table.setModel(self.driver_model)
        driver_table.setAlternatingRowColors(True)
        driver_table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        driver_table.setSelectionMode(QTableView.SelectionMode.ExtendedSelection)
        self.driver_table = driver_table

        bulk_row = QHBoxLayout()
        self.bulk_shock = QDoubleSpinBox()
        self.bulk_shock.setRange(-5.0, 5.0)
        self.bulk_shock.setSingleStep(0.01)
        self.bulk_shock.setValue(-0.05)
        apply_bulk_btn = QPushButton("Apply Shock To Selected")
        apply_bulk_btn.clicked.connect(self._apply_bulk_to_selected)
        bulk_row.addWidget(QLabel("Shock"))
        bulk_row.addWidget(self.bulk_shock)
        bulk_row.addWidget(apply_bulk_btn)

        bottom_layout.addLayout(search_row)
        bottom_layout.addWidget(driver_table)
        bottom_layout.addLayout(bulk_row)

        recon_group = QGroupBox("Top-Down ↔ Bottom-Up Reconciliation")
        recon_layout = QFormLayout(recon_group)
        self.blend_slider = QSlider(Qt.Orientation.Horizontal)
        self.blend_slider.setRange(0, 100)
        self.blend_slider.setValue(60)
        self.blend_label = QLabel("Top-Down Weight: 60%")
        self.blend_slider.valueChanged.connect(lambda v: self.blend_label.setText(f"Top-Down Weight: {v}%"))
        blend_btn = QPushButton("Blend Into Driver Shocks")
        blend_btn.clicked.connect(self._blend_shocks)

        self.recon_report = QTextEdit()
        self.recon_report.setReadOnly(True)
        self.recon_report.setMinimumHeight(70)

        recon_layout.addRow(self.blend_label, self.blend_slider)
        recon_layout.addRow("", blend_btn)
        recon_layout.addRow("Narrative Consistency", self.recon_report)

        split = QSplitter(Qt.Orientation.Vertical)
        top_container = QWidget()
        top_container_layout = QVBoxLayout(top_container)
        top_container_layout.addWidget(top_group)
        top_container_layout.addWidget(shock_group)

        bottom_container = QWidget()
        bottom_container_layout = QVBoxLayout(bottom_container)
        bottom_container_layout.addWidget(bottom_group)
        bottom_container_layout.addWidget(recon_group)

        split.addWidget(top_container)
        split.addWidget(bottom_container)
        split.setSizes([650, 550])

        root.addWidget(split)

    def _initialize_defaults(self) -> None:
        scenario = self.state.ensure_scenario()
        self.scenario_name.setText(scenario.metadata.name)
        self.narrative.setPlainText(scenario.narrative.text)
        self._refresh_asset_shocks()
        self.driver_model.set_frame(scenario.shocks.risk_driver_shocks.head(5000))

    def _current_theme_weights(self) -> dict[str, float]:
        weights = {k: float(v.value()) for k, v in self.theme_inputs.items()}
        total = sum(weights.values())
        if total == 0:
            return {k: 0.0 for k in weights}
        return {k: round(v / total, 4) for k, v in weights.items()}

    def _apply_top_down(self) -> None:
        scenario = self.state.ensure_scenario()
        scenario.metadata.name = self.scenario_name.text().strip() or scenario.metadata.name
        warnings = self.state.apply_top_down_settings(
            narrative=self.narrative.toPlainText().strip(),
            theme_weights=self._current_theme_weights(),
            severity_scale=float(self.severity_scale.value()),
            horizon_days=int(self.horizon_days.value()),
            calibration_method=self.calibration_combo.currentText(),
            template=self.template_combo.currentText(),
        )
        self._refresh_asset_shocks()
        if warnings:
            self.coherence_box.setPlainText("\n".join(f"- {w}" for w in warnings))
        else:
            self.coherence_box.setPlainText("No coherence conflicts detected.")
        self.signals.scenario_changed.emit()
        self.signals.status_message.emit("Top-down scenario settings updated.")

    def _refresh_asset_shocks(self) -> None:
        scenario = self.state.ensure_scenario()
        rows = []
        for ac, params in scenario.shocks.asset_class_shocks.items():
            for k, v in params.items():
                rows.append({"asset_class": ac, "parameter": k, "shock": v})
        self.asset_shock_model.set_frame(pd.DataFrame(rows))

    def _search_drivers(self) -> None:
        query = self.search_input.text().strip()
        frame = search_risk_drivers(self.state.data_bundle.risk_drivers, query=query, limit=5000)

        scenario = self.state.ensure_scenario()
        shocks = scenario.shocks.risk_driver_shocks[["driver_id", "shock", "lock"]] if not scenario.shocks.risk_driver_shocks.empty else pd.DataFrame(columns=["driver_id", "shock", "lock"])
        merged = frame.merge(shocks, on="driver_id", how="left")
        merged["shock"] = merged["shock"].fillna(0.0)
        merged["lock"] = merged["lock"].fillna(False)
        self.driver_model.set_frame(merged)

    def _apply_bulk_to_selected(self) -> None:
        scenario = self.state.ensure_scenario()
        if scenario.shocks.risk_driver_shocks.empty:
            QMessageBox.warning(self, "No Shock Table", "No bottom-up shock table available.")
            return

        selected_rows = sorted({ix.row() for ix in self.driver_table.selectionModel().selectedRows()})
        if not selected_rows:
            QMessageBox.information(self, "No Selection", "Select one or more rows in the driver table.")
            return

        visible = self.driver_model.frame.reset_index(drop=True)
        ids = visible.loc[selected_rows, "driver_id"].astype(str).tolist()
        shock_val = float(self.bulk_shock.value())

        shock_table = scenario.shocks.risk_driver_shocks.copy()
        unlocked_ids = [x for x in ids if x not in scenario.shocks.locked_drivers]
        scenario.shocks.risk_driver_shocks = apply_bulk_shock(shock_table, unlocked_ids, shock_val)

        self._search_drivers()
        self.signals.scenario_changed.emit()
        self.signals.status_message.emit(f"Applied bulk shock={shock_val:.4f} to {len(unlocked_ids)} drivers.")

    def _import_driver_shocks(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Driver Shock File",
            str(Path.cwd()),
            "Data Files (*.csv *.xlsx *.xls *.json *.parquet)",
        )
        if not file_path:
            return

        try:
            frame = self.file_importer.load(file_path)
            required = {"driver_id", "shock"}
            if not required.issubset(set(frame.columns)):
                missing = required - set(frame.columns)
                raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
            if "lock" not in frame.columns:
                frame["lock"] = False
            self.state.ensure_scenario().shocks.risk_driver_shocks = frame[["driver_id", "shock", "lock"]].copy()
            self._search_drivers()
            self.signals.scenario_changed.emit()
            self.signals.status_message.emit(f"Imported {len(frame):,} driver shocks.")
        except Exception as exc:
            QMessageBox.critical(self, "Import Error", str(exc))

    def _mock_ai_narrative(self) -> None:
        narrative = (
            "Stagflationary shock driven by tariff escalation and policy credibility concerns. "
            "Rates reprice sharply higher in the front-end, equities correct with growth-sector underperformance, "
            "credit spreads widen across IG/HY, USD strengthens against EM FX, and volatility regimes shift toward crisis correlations."
        )
        self.narrative.setPlainText(narrative)

    def _blend_shocks(self) -> None:
        scenario = self.state.ensure_scenario()
        if scenario.shocks.risk_driver_shocks.empty:
            QMessageBox.warning(self, "No Driver Shocks", "Import or generate bottom-up shocks first.")
            return

        td_rows = []
        for _, row in self.state.data_bundle.risk_drivers[["driver_id", "asset_class"]].iterrows():
            ac = row["asset_class"]
            params = scenario.shocks.asset_class_shocks.get(ac, {})
            ds = float(
                params.get("index_pct")
                or params.get("spot_pct")
                or params.get("parallel_shift_bp", 0.0) / 10000.0
                or params.get("energy_pct", 0.0)
            )
            td_rows.append({"driver_id": row["driver_id"], "shock": ds})

        top = pd.DataFrame(td_rows)
        bottom = scenario.shocks.risk_driver_shocks[["driver_id", "shock"]].copy()

        blend_weight = self.blend_slider.value() / 100.0
        blended = blend_shocks(top_down_shocks=top, bottom_up_shocks=bottom, weight_top_down=blend_weight)

        if "lock" in scenario.shocks.risk_driver_shocks.columns:
            locks = scenario.shocks.risk_driver_shocks[["driver_id", "lock"]]
            blended = blended.merge(locks, on="driver_id", how="left")
            blended["lock"] = blended["lock"].fillna(False)
        else:
            blended["lock"] = False

        # Keep locked values untouched from bottom-up table.
        locked = set(blended.loc[blended["lock"], "driver_id"].tolist())
        if locked:
            prior = scenario.shocks.risk_driver_shocks.set_index("driver_id")
            for did in locked:
                if did in prior.index:
                    blended.loc[blended["driver_id"] == did, "shock"] = float(prior.loc[did, "shock"])

        scenario.shocks.risk_driver_shocks = blended[["driver_id", "shock", "lock"]]
        self.recon_report.setPlainText(
            "Blended top-down and bottom-up shocks successfully. "
            "Run calculations to refresh discrepancy and narrative consistency diagnostics."
        )
        self._search_drivers()
        self.signals.scenario_changed.emit()
        self.signals.status_message.emit("Reconciliation blend applied to driver-level shocks.")
