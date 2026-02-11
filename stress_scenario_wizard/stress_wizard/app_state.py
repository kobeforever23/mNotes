from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import getpass
import uuid

import pandas as pd

from stress_wizard.calc.attribution import (
    by_asset_class,
    by_book,
    by_desk,
    by_geography,
    by_position,
    by_risk_factor,
    by_tenor_bucket,
)
from stress_wizard.calc.engine import CalculationConfig, compute_pnl, portfolio_summary
from stress_wizard.calc.shift_analysis import marginal_contribution, sensitivity_table, tornado_data
from stress_wizard.data.demo_data import generate_demo_bundle, generate_sample_driver_shocks
from stress_wizard.models import (
    CalibrationMethod,
    DataBundle,
    NarrativeConfig,
    Scenario,
    ScenarioApproach,
    ScenarioMetadata,
    SeverityTier,
    ShockConfig,
)
from stress_wizard.scenario.top_down import TopDownConfig, coherence_checks, generate_asset_class_shocks


@dataclass(slots=True)
class AnalysisOutputs:
    results: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    summary: dict = field(default_factory=dict)
    attribution: dict[str, pd.DataFrame] = field(default_factory=dict)
    sensitivity: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    tornado: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    marginal: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())


@dataclass(slots=True)
class AppState:
    data_bundle: DataBundle = field(default_factory=lambda: generate_demo_bundle())
    scenario: Scenario | None = None
    outputs: AnalysisOutputs = field(default_factory=AnalysisOutputs)

    def ensure_scenario(self) -> Scenario:
        if self.scenario is None:
            self.create_new_scenario("Demo Stress Scenario")
        return self.scenario

    def create_new_scenario(self, name: str) -> Scenario:
        metadata = ScenarioMetadata(
            scenario_id=f"SCN-{datetime.now():%Y%m%d}-{uuid.uuid4().hex[:6].upper()}",
            name=name,
            author=getpass.getuser(),
            created_at=datetime.now(),
            severity=SeverityTier.SEVERE,
            horizon_days=10,
            approach=ScenarioApproach.HYBRID,
            calibration=CalibrationMethod.HISTORICAL,
            as_of_date=datetime.now(),
        )

        top_down = TopDownConfig(
            narrative="Baseline severe macro stress with rates up, equities down, and spread widening.",
            theme_weights={"Recession": 0.4, "Stagflation": 0.4, "Geopolitical": 0.2},
            severity_scale=1.0,
            horizon_days=10,
            calibration_method="Historical",
            transmission_template="Rate Hike",
        )
        asset_shocks = generate_asset_class_shocks(top_down)
        driver_shocks = generate_sample_driver_shocks(self.data_bundle.risk_drivers, n=1200)

        self.scenario = Scenario(
            metadata=metadata,
            narrative=NarrativeConfig(
                text=top_down.narrative,
                themes=top_down.theme_weights,
                transmission_links=[],
            ),
            shocks=ShockConfig(
                asset_class_shocks=asset_shocks,
                risk_driver_shocks=driver_shocks,
                locked_drivers=set(driver_shocks.loc[driver_shocks["lock"], "driver_id"].tolist()),
            ),
        )
        return self.scenario

    def apply_top_down_settings(
        self,
        narrative: str,
        theme_weights: dict[str, float],
        severity_scale: float,
        horizon_days: int,
        calibration_method: str,
        template: str,
    ) -> list[str]:
        scenario = self.ensure_scenario()
        config = TopDownConfig(
            narrative=narrative,
            theme_weights=theme_weights,
            severity_scale=severity_scale,
            horizon_days=horizon_days,
            calibration_method=calibration_method,
            transmission_template=template,
        )
        scenario.narrative.text = narrative
        scenario.narrative.themes = theme_weights
        scenario.metadata.horizon_days = horizon_days
        scenario.shocks.asset_class_shocks = generate_asset_class_shocks(config)
        return coherence_checks(scenario.shocks.asset_class_shocks)

    def regenerate_risk_drivers(self, count: int) -> None:
        self.data_bundle = generate_demo_bundle(risk_driver_count=count)
        if self.scenario is not None:
            self.scenario.shocks.risk_driver_shocks = generate_sample_driver_shocks(self.data_bundle.risk_drivers, n=min(5000, count // 20))

    def run_calculation(self, correlation_regime: float = 0.35, liquidity_bps: float = 12.0, funding_spread_bps: float = 25.0) -> AnalysisOutputs:
        scenario = self.ensure_scenario()
        cfg = CalculationConfig(
            horizon_days=scenario.metadata.horizon_days,
            correlation_regime=correlation_regime,
            liquidity_bps=liquidity_bps,
            funding_spread_bps=funding_spread_bps,
        )

        results = compute_pnl(
            positions=self.data_bundle.positions,
            sensitivities=self.data_bundle.sensitivities,
            asset_class_shocks=scenario.shocks.asset_class_shocks,
            driver_shocks=scenario.shocks.risk_driver_shocks,
            config=cfg,
        )

        attrib = {
            "asset_class": by_asset_class(results),
            "risk_factor": by_risk_factor(results),
            "desk": by_desk(results),
            "book": by_book(results),
            "position": by_position(results),
            "geography": by_geography(results),
            "tenor": by_tenor_bucket(results),
        }

        sens = sensitivity_table(
            self.data_bundle.positions,
            self.data_bundle.sensitivities,
            scenario.shocks.asset_class_shocks,
        )

        outputs = AnalysisOutputs(
            results=results,
            summary=portfolio_summary(results),
            attribution=attrib,
            sensitivity=sens,
            tornado=tornado_data(sens),
            marginal=marginal_contribution(results),
        )
        self.outputs = outputs
        return outputs
