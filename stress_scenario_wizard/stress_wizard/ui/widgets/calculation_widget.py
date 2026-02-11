from __future__ import annotations

import pandas as pd
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableView,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from stress_wizard.app_state import AppState
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.pandas_model import LazyDataFrameModel


class CalculationWidget(QWidget):
    def __init__(self, state: AppState, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.signals = signals

        self.results_model = LazyDataFrameModel(pd.DataFrame())
        self.attrib_model = LazyDataFrameModel(pd.DataFrame())
        self.shift_model = LazyDataFrameModel(pd.DataFrame())

        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)

        config_group = QGroupBox("Calculation Engine")
        cfg = QFormLayout(config_group)

        self.corr_regime = QDoubleSpinBox()
        self.corr_regime.setRange(0.0, 1.0)
        self.corr_regime.setSingleStep(0.05)
        self.corr_regime.setValue(0.35)

        self.liquidity_bps = QDoubleSpinBox()
        self.liquidity_bps.setRange(0.0, 500.0)
        self.liquidity_bps.setValue(12.0)

        self.funding_bps = QDoubleSpinBox()
        self.funding_bps.setRange(0.0, 1000.0)
        self.funding_bps.setValue(25.0)

        run_btn = QPushButton("Run Stress Calculation")
        run_btn.clicked.connect(self._run)

        cfg.addRow("Correlation Regime (0-1)", self.corr_regime)
        cfg.addRow("Liquidity Widening (bps)", self.liquidity_bps)
        cfg.addRow("Funding Stress (bps)", self.funding_bps)
        cfg.addRow("", run_btn)

        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_text.setMinimumHeight(120)

        attrib_row = QHBoxLayout()
        self.attrib_view = QComboBox()
        self.attrib_view.addItems(["asset_class", "risk_factor", "desk", "book", "position", "geography", "tenor"])
        self.attrib_view.currentTextChanged.connect(self._refresh_attribution_view)
        attrib_row.addWidget(QLabel("Attribution View"))
        attrib_row.addWidget(self.attrib_view)

        results_table = QTableView()
        results_table.setModel(self.results_model)
        results_table.setAlternatingRowColors(True)

        attrib_table = QTableView()
        attrib_table.setModel(self.attrib_model)
        attrib_table.setAlternatingRowColors(True)

        shift_table = QTableView()
        shift_table.setModel(self.shift_model)
        shift_table.setAlternatingRowColors(True)

        root.addWidget(config_group)
        root.addWidget(QLabel("Portfolio Summary"))
        root.addWidget(self.summary_text)
        root.addLayout(attrib_row)
        root.addWidget(QLabel("Attribution"))
        root.addWidget(attrib_table, stretch=1)
        root.addWidget(QLabel("Shift / Sensitivity Table"))
        root.addWidget(shift_table, stretch=1)
        root.addWidget(QLabel("Position-Level Drilldown"))
        root.addWidget(results_table, stretch=1)

    def _run(self) -> None:
        outputs = self.state.run_calculation(
            correlation_regime=float(self.corr_regime.value()),
            liquidity_bps=float(self.liquidity_bps.value()),
            funding_spread_bps=float(self.funding_bps.value()),
        )

        summary_lines = [
            f"Position Count: {outputs.summary.get('position_count', 0):,}",
            f"Loss-Making Positions: {outputs.summary.get('loss_positions', 0):,}",
            f"Total P&L: {outputs.summary.get('pnl_total', 0.0):,.2f}",
            f"Delta P&L: {outputs.summary.get('pnl_delta', 0.0):,.2f}",
            f"Gamma P&L: {outputs.summary.get('pnl_gamma', 0.0):,.2f}",
            f"Vega P&L: {outputs.summary.get('pnl_vega', 0.0):,.2f}",
            f"Rho P&L: {outputs.summary.get('pnl_rho', 0.0):,.2f}",
            f"CS01 P&L: {outputs.summary.get('pnl_cs01', 0.0):,.2f}",
            f"Theta P&L: {outputs.summary.get('pnl_theta', 0.0):,.2f}",
            f"Cross-Gamma P&L: {outputs.summary.get('pnl_cross_gamma', 0.0):,.2f}",
            f"Funding Adjustment: {outputs.summary.get('pnl_funding', 0.0):,.2f}",
            f"Liquidity Adjustment: {outputs.summary.get('pnl_liquidity', 0.0):,.2f}",
        ]
        self.summary_text.setPlainText("\n".join(summary_lines))

        self.results_model.set_frame(outputs.results.head(12000))
        self.shift_model.set_frame(outputs.sensitivity.head(1000))
        self._refresh_attribution_view()

        self.signals.calculation_complete.emit()
        self.signals.status_message.emit("Stress calculation completed.")

    def _refresh_attribution_view(self) -> None:
        view = self.attrib_view.currentText()
        if view in self.state.outputs.attribution:
            self.attrib_model.set_frame(self.state.outputs.attribution[view])
        else:
            self.attrib_model.set_frame(pd.DataFrame())
