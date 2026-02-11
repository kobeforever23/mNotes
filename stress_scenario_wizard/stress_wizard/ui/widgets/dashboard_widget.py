from __future__ import annotations

import numpy as np
import pandas as pd
from PySide6.QtWidgets import QTabWidget, QVBoxLayout, QWidget
import plotly.express as px

from stress_wizard.app_state import AppState
from stress_wizard.ui.signals import AppSignals
from stress_wizard.ui.widgets.plotly_view import PlotlyWidget, make_heatmap, make_tornado, make_waterfall


class DashboardWidget(QWidget):
    def __init__(self, state: AppState, signals: AppSignals, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.state = state
        self.signals = signals
        self._build_ui()
        self.signals.calculation_complete.connect(self.refresh)

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        self.tabs = QTabWidget()

        self.heatmap = PlotlyWidget()
        self.waterfall = PlotlyWidget()
        self.tornado = PlotlyWidget()
        self.curve = PlotlyWidget()
        self.corr = PlotlyWidget()
        self.coverage = PlotlyWidget()

        self.tabs.addTab(self.heatmap, "Scenario Heatmap")
        self.tabs.addTab(self.waterfall, "Waterfall")
        self.tabs.addTab(self.tornado, "Tornado")
        self.tabs.addTab(self.curve, "Yield Curve")
        self.tabs.addTab(self.corr, "Correlation Matrix")
        self.tabs.addTab(self.coverage, "Driver Coverage")

        root.addWidget(self.tabs)

    def refresh(self) -> None:
        outputs = self.state.outputs
        if outputs.results.empty:
            return

        ac = outputs.attribution.get("asset_class", pd.DataFrame())
        if not ac.empty:
            scales = pd.DataFrame(
                {
                    "severity": ["Moderate", "Severe", "Extreme"],
                    "mult": [0.7, 1.0, 1.6],
                }
            )
            heat_rows = []
            for _, row in ac.iterrows():
                for _, s in scales.iterrows():
                    heat_rows.append(
                        {
                            "asset_class": row["asset_class"],
                            "severity": s["severity"],
                            "pnl": float(row["pnl"] * s["mult"]),
                        }
                    )
            heat_df = pd.DataFrame(heat_rows)
            self.heatmap.set_figure(make_heatmap(heat_df, x="severity", y="asset_class", value="pnl", title="Asset Class x Severity P&L"))

        rf = outputs.attribution.get("risk_factor", pd.DataFrame())
        if not rf.empty:
            labels = rf["risk_factor"].astype(str).tolist()
            values = rf["pnl"].astype(float).tolist()
            self.waterfall.set_figure(make_waterfall(labels, values, title="Risk Factor Waterfall"))

        if not outputs.tornado.empty:
            self.tornado.set_figure(make_tornado(outputs.tornado, title="Shock Sensitivity Tornado"))

        # Yield curve visualization from rates shock parameters.
        scenario = self.state.ensure_scenario()
        rates = scenario.shocks.asset_class_shocks.get("Rates", {})
        base = np.array([2.2, 2.25, 2.3, 2.35, 2.45, 2.5, 2.55, 2.58, 2.6, 2.63, 2.65])
        tenors = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
        parallel = float(rates.get("parallel_shift_bp", 0.0)) / 100.0
        twist = float(rates.get("twist_bp", 0.0)) / 100.0
        adjustments = np.linspace(-twist, twist, len(base))
        stressed = base + parallel + adjustments
        curve_df = pd.DataFrame(
            {
                "tenor": tenors * 2,
                "yield": np.concatenate([base, stressed]),
                "curve": ["Base"] * len(base) + ["Stressed"] * len(base),
            }
        )
        fig_curve = px.line(curve_df, x="tenor", y="yield", color="curve", markers=True, title="Yield Curve Base vs Stressed")
        fig_curve.update_layout(template="plotly_dark")
        self.curve.set_figure(fig_curve)

        # Correlation matrix before/after stress.
        assets = ["Rates", "FX", "Equities", "Credit", "Commodities", "Volatility"]
        rng = np.random.default_rng(7)
        base_corr = rng.uniform(-0.3, 0.5, (len(assets), len(assets)))
        base_corr = (base_corr + base_corr.T) / 2
        np.fill_diagonal(base_corr, 1.0)
        crisis = np.clip(base_corr + 0.35, -1.0, 1.0)
        corr_df = pd.DataFrame(crisis - base_corr, index=assets, columns=assets)
        fig_corr = px.imshow(corr_df, text_auto=True, color_continuous_scale="RdBu", zmin=-1, zmax=1, title="Correlation Shift (Crisis - Base)")
        fig_corr.update_layout(template="plotly_dark")
        self.corr.set_figure(fig_corr)

        # Coverage map: shocked vs unshocked by asset class.
        drivers = self.state.data_bundle.risk_drivers[["driver_id", "asset_class"]].copy()
        shocked = set(scenario.shocks.risk_driver_shocks.loc[scenario.shocks.risk_driver_shocks["shock"].abs() > 1e-12, "driver_id"].tolist())
        drivers["shocked"] = drivers["driver_id"].isin(shocked)
        cov = drivers.groupby(["asset_class", "shocked"], as_index=False).size()
        cov["status"] = np.where(cov["shocked"], "Shocked", "Unshocked")
        fig_cov = px.bar(cov, x="asset_class", y="size", color="status", barmode="stack", title="Risk Driver Coverage Map")
        fig_cov.update_layout(template="plotly_dark")
        self.coverage.set_figure(fig_cov)
