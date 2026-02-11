from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QKeySequence
from PySide6.QtWidgets import (
    QDockWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QStatusBar,
    QTabWidget,
)

from stress_wizard.app_state import AppState
from stress_wizard.config import AppSettings, save_settings
from stress_wizard.exporter.persistence import (
    append_audit_log,
    create_scenario_structure,
    write_driver_shocks,
    write_governance_artifacts,
    write_narrative,
    write_results_workbook,
    write_scenario_config,
)
from stress_wizard.exporter.reporting import (
    build_narrative_document,
    build_shock_justification_table,
    export_pdf_summary,
    export_pptx_summary,
)
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.calculation_widget import CalculationWidget
from stress_wizard.ui.widgets.dashboard_widget import DashboardWidget
from stress_wizard.ui.widgets.data_ingestion_widget import DataIngestionWidget
from stress_wizard.ui.widgets.governance_widget import GovernanceWidget
from stress_wizard.ui.widgets.library_widget import ScenarioLibraryWidget
from stress_wizard.ui.widgets.scenario_designer_widget import ScenarioDesignerWidget


class MainWindow(QMainWindow):
    def __init__(self, settings: AppSettings, parent=None) -> None:
        super().__init__(parent)
        self.settings = settings
        self.state = AppState()
        self.signals = AppSignals()

        self.last_save_time: datetime | None = None
        self.current_scenario_dir: Path | None = None

        self.undo_stack: list[str] = []
        self.redo_stack: list[str] = []

        self._init_ui()
        self._connect_signals()
        self._setup_autosave()
        self._load_recovery()

    def _init_ui(self) -> None:
        self.setWindowTitle("Stress Scenario Generation Wizard")
        self.resize(1680, 980)

        self.tabs = QTabWidget(self)

        self.ingestion_widget = DataIngestionWidget(self.state, self.signals, self)
        self.scenario_widget = ScenarioDesignerWidget(self.state, self.signals, self)
        self.calc_widget = CalculationWidget(self.state, self.signals, self)
        self.dashboard_widget = DashboardWidget(self.state, self.signals, self)
        self.library_widget = ScenarioLibraryWidget(self.settings, self)

        self.tabs.addTab(self.ingestion_widget, "1) Ingestion")
        self.tabs.addTab(self.scenario_widget, "2) Scenario Design")
        self.tabs.addTab(self.calc_widget, "3) Calculation")
        self.tabs.addTab(self.dashboard_widget, "4) Dashboard")
        self.tabs.addTab(self.library_widget, "8) Scenario Library")

        self.setCentralWidget(self.tabs)

        self.governance_widget = GovernanceWidget(self.state, self.settings, self.signals, self)
        self.governance_dock = QDockWidget("Governance Panel", self)
        self.governance_dock.setWidget(self.governance_widget)
        self.governance_dock.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.governance_dock)

        self.status = QStatusBar(self)
        self.setStatusBar(self.status)
        self._refresh_status("Ready")

        self._init_menu()

    def _init_menu(self) -> None:
        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        new_action = QAction("New Scenario", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self._new_scenario)
        file_menu.addAction(new_action)

        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self._save)
        file_menu.addAction(save_action)

        save_as_action = QAction("Save As", self)
        save_as_action.triggered.connect(self._save_as)
        file_menu.addAction(save_as_action)

        export_action = QAction("Export Package", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self._export)
        file_menu.addAction(export_action)

        quit_action = QAction("Exit", self)
        quit_action.setShortcut(QKeySequence.StandardKey.Quit)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)

        edit_menu = menu.addMenu("Edit")
        undo_action = QAction("Undo Shock Change", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self._undo)
        edit_menu.addAction(undo_action)

        redo_action = QAction("Redo Shock Change", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self._redo)
        edit_menu.addAction(redo_action)

        view_menu = menu.addMenu("View")
        toggle_gov = QAction("Toggle Governance Dock", self)
        toggle_gov.triggered.connect(lambda: self.governance_dock.setVisible(not self.governance_dock.isVisible()))
        view_menu.addAction(toggle_gov)

    def _connect_signals(self) -> None:
        self.signals.status_message.connect(self._refresh_status)
        self.signals.scenario_changed.connect(self._snapshot_for_undo)
        self.signals.calculation_complete.connect(lambda: self._refresh_status("Calculation complete"))
        self.signals.governance_changed.connect(self._sync_governance_to_exports)

    def _setup_autosave(self) -> None:
        self.autosave_timer = QTimer(self)
        self.autosave_timer.timeout.connect(self._autosave)
        if self.settings.autosave_enabled:
            self.autosave_timer.start(max(15, self.settings.autosave_interval_seconds) * 1000)

    def _refresh_status(self, message: str) -> None:
        db_state = "DB: Demo/File"
        portfolio_state = f"Positions: {len(self.state.data_bundle.positions):,}"
        saved = self.last_save_time.strftime("%H:%M:%S") if self.last_save_time else "never"
        self.status.showMessage(f"{message} | {db_state} | {portfolio_state} | Last Save: {saved}")

    def _snapshot_for_undo(self) -> None:
        scenario = self.state.ensure_scenario()
        payload = scenario.shocks.risk_driver_shocks.to_json(orient="records")
        if not self.undo_stack or self.undo_stack[-1] != payload:
            self.undo_stack.append(payload)
            if len(self.undo_stack) > 40:
                self.undo_stack.pop(0)
            self.redo_stack.clear()

    def _restore_snapshot(self, payload: str) -> None:
        frame = pd.read_json(payload)
        scenario = self.state.ensure_scenario()
        scenario.shocks.risk_driver_shocks = frame
        self.scenario_widget._search_drivers()  # noqa: SLF001
        self._refresh_status("Shock table restored")

    def _undo(self) -> None:
        if len(self.undo_stack) < 2:
            return
        current = self.undo_stack.pop()
        self.redo_stack.append(current)
        self._restore_snapshot(self.undo_stack[-1])

    def _redo(self) -> None:
        if not self.redo_stack:
            return
        payload = self.redo_stack.pop()
        self.undo_stack.append(payload)
        self._restore_snapshot(payload)

    def _new_scenario(self) -> None:
        self.state.create_new_scenario("Untitled Stress Scenario")
        self.scenario_widget._initialize_defaults()  # noqa: SLF001
        self._refresh_status("Created new scenario")

    def _default_root(self) -> Path:
        root = Path(self.settings.root_path)
        root.mkdir(parents=True, exist_ok=True)
        return root

    def _save(self) -> None:
        scenario = self.state.ensure_scenario()
        scenario_dir = create_scenario_structure(self._default_root(), scenario)
        self.current_scenario_dir = scenario_dir

        write_scenario_config(scenario_dir, scenario)
        write_driver_shocks(scenario_dir, scenario.shocks.risk_driver_shocks)

        outputs = self.state.outputs
        if not outputs.results.empty:
            sheets = {
                "summary": pd.DataFrame([outputs.summary]),
                "by_asset_class": outputs.attribution.get("asset_class", pd.DataFrame()),
                "by_desk": outputs.attribution.get("desk", pd.DataFrame()),
                "by_position": outputs.attribution.get("position", pd.DataFrame()).head(50000),
                "shift_analysis": outputs.sensitivity,
            }
            write_results_workbook(scenario_dir, sheets)

        narrative_md = build_narrative_document(
            scenario_name=scenario.metadata.name,
            economic_rationale=scenario.narrative.text,
            transmission_logic="Macro variables propagate across rates, equities, credit, FX, and volatility through configured transmission links.",
            calibration_method=scenario.metadata.calibration.value,
            assumptions=[
                "Taylor expansion approximation used for non-linear pricing impacts.",
                "Correlation regime slider controls cross-term intensification.",
                "Funding and liquidity adjustments scaled to notional exposures.",
            ],
            limitations=[
                "Some instrument-level optionality may require full revaluation for highest fidelity.",
                "Data quality issues can materially change attribution outputs.",
            ],
        )
        write_narrative(scenario_dir, narrative_md)

        gov_state = self.governance_widget.workflow.load_state(scenario.metadata.scenario_id)
        comments = self.governance_widget.workflow.latest_comments(scenario.metadata.scenario_id)
        write_governance_artifacts(scenario_dir, gov_state, comments, distribution_log=[])

        append_audit_log(scenario_dir, action="save", actor=scenario.metadata.author, details={"scenario_id": scenario.metadata.scenario_id})

        self.last_save_time = datetime.now()
        self._refresh_status("Scenario saved")
        self.library_widget.refresh()

    def _save_as(self) -> None:
        chosen = QFileDialog.getExistingDirectory(self, "Select Save Root", self.settings.root_path)
        if not chosen:
            return
        self.settings.root_path = chosen
        save_settings(self.settings)
        self._save()

    def _export(self) -> None:
        scenario = self.state.ensure_scenario()
        gov_state = self.governance_widget.workflow.load_state(scenario.metadata.scenario_id)
        if self.settings.governance.mandatory_export_approval and gov_state.get("state") != "Approved":
            QMessageBox.warning(self, "Governance Block", "Mandatory approval is enabled. Scenario must be Approved before export.")
            return

        if self.current_scenario_dir is None:
            self._save()
        assert self.current_scenario_dir is not None

        outputs = self.state.outputs
        summary_lines = [
            f"Scenario: {scenario.metadata.name}",
            f"Severity: {scenario.metadata.severity.value}",
            f"Horizon: {scenario.metadata.horizon_days} days",
            f"Total P&L: {outputs.summary.get('pnl_total', 0.0):,.2f}",
            f"Approval State: {gov_state.get('state')}",
        ]
        if gov_state.get("state") == "Approved":
            summary_lines.append(f"Governance Stamp: APPROVED | Version {gov_state.get('version', 1)}")

        pdf_path = self.current_scenario_dir / "scenario_report.pdf"
        pptx_path = self.current_scenario_dir / "scenario_summary.pptx"

        export_pdf_summary(pdf_path, title="Stress Scenario Report", summary_lines=summary_lines)
        export_pptx_summary(pptx_path, title=f"{scenario.metadata.name} Summary", bullets=summary_lines)

        if not outputs.results.empty:
            outputs.results.to_csv(self.current_scenario_dir / "results_raw.csv", index=False)
            outputs.results.to_parquet(self.current_scenario_dir / "results_raw.parquet", index=False)
            shock_just = build_shock_justification_table(scenario.shocks.risk_driver_shocks)
            shock_just.to_csv(self.current_scenario_dir / "shock_justification.csv", index=False)

        append_audit_log(self.current_scenario_dir, action="export", actor=scenario.metadata.author, details={"formats": ["pdf", "pptx", "csv", "parquet"]})
        self._refresh_status("Export completed")
        QMessageBox.information(self, "Export Complete", f"Exported files to:\n{self.current_scenario_dir}")

    def _sync_governance_to_exports(self) -> None:
        if self.current_scenario_dir is None:
            return
        scenario_id = self.state.ensure_scenario().metadata.scenario_id
        gov_state = self.governance_widget.workflow.load_state(scenario_id)
        comments = self.governance_widget.workflow.latest_comments(scenario_id)
        write_governance_artifacts(self.current_scenario_dir, gov_state, comments, distribution_log=[])

    def _autosave(self) -> None:
        try:
            self._save()
        except Exception:
            # Keep autosave non-blocking in UI path.
            pass

    def _recovery_file(self) -> Path:
        return Path(".session_recovery.json")

    def _load_recovery(self) -> None:
        file = self._recovery_file()
        if not self.settings.save_last_session or not file.exists():
            return
        try:
            payload = json.loads(file.read_text(encoding="utf-8"))
            name = payload.get("scenario_name")
            if name:
                self.state.create_new_scenario(name)
                self.scenario_widget._initialize_defaults()  # noqa: SLF001
        except Exception:
            return

    def _write_recovery(self) -> None:
        if not self.settings.save_last_session:
            return
        scenario = self.state.ensure_scenario()
        payload = {
            "scenario_name": scenario.metadata.name,
            "scenario_id": scenario.metadata.scenario_id,
            "timestamp": datetime.now().isoformat(),
        }
        self._recovery_file().write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def closeEvent(self, event) -> None:  # noqa: N802
        self._write_recovery()
        super().closeEvent(event)
