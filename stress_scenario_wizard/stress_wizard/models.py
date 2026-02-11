from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

import pandas as pd


class SeverityTier(str, Enum):
    MODERATE = "Moderate"
    SEVERE = "Severe"
    EXTREME = "Extreme"
    CUSTOM = "Custom"


class ScenarioApproach(str, Enum):
    TOP_DOWN = "Top-Down"
    BOTTOM_UP = "Bottom-Up"
    HYBRID = "Hybrid"


class CalibrationMethod(str, Enum):
    HISTORICAL = "Historical"
    STATISTICAL = "Statistical"
    HYPOTHETICAL = "Hypothetical"
    HYBRID = "Hybrid"


@dataclass(slots=True)
class ScenarioMetadata:
    scenario_id: str
    name: str
    author: str
    created_at: datetime
    severity: SeverityTier
    horizon_days: int
    approach: ScenarioApproach
    calibration: CalibrationMethod
    as_of_date: datetime


@dataclass(slots=True)
class NarrativeConfig:
    text: str = ""
    themes: dict[str, float] = field(default_factory=dict)
    transmission_links: list[dict[str, Any]] = field(default_factory=list)


@dataclass(slots=True)
class ShockConfig:
    asset_class_shocks: dict[str, dict[str, float]] = field(default_factory=dict)
    risk_driver_shocks: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())
    locked_drivers: set[str] = field(default_factory=set)


@dataclass(slots=True)
class Scenario:
    metadata: ScenarioMetadata
    narrative: NarrativeConfig = field(default_factory=NarrativeConfig)
    shocks: ShockConfig = field(default_factory=ShockConfig)


@dataclass(slots=True)
class DataBundle:
    positions: pd.DataFrame
    sensitivities: pd.DataFrame
    market_data: pd.DataFrame
    risk_drivers: pd.DataFrame


REQUIRED_POSITION_COLUMNS = {
    "instrument_id",
    "asset_class",
    "sub_asset_class",
    "desk",
    "book",
    "notional",
    "direction",
    "maturity",
    "currency",
}


REQUIRED_SENS_COLUMNS = {
    "instrument_id",
    "delta",
    "gamma",
    "vega",
    "rho",
    "cs01",
    "dv01",
    "theta",
    "convexity",
}


REQUIRED_MARKET_COLUMNS = {
    "driver_id",
    "asset_class",
    "level",
    "as_of",
}


REQUIRED_DRIVER_COLUMNS = {
    "driver_id",
    "name",
    "asset_class",
    "geography",
    "tenor",
    "sector",
}
