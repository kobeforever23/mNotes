from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd


TRANSMISSION_TEMPLATES = {
    "Rate Hike": [
        ("Policy Rates", "Sovereign Yields", 0.9),
        ("Sovereign Yields", "Equity Index", -0.5),
        ("Sovereign Yields", "Credit Spreads", 0.4),
        ("Sovereign Yields", "USD", 0.3),
        ("Equity Index", "Equity Vol", 0.6),
    ],
    "Credit Crunch": [
        ("Funding Stress", "Credit Spreads", 1.0),
        ("Credit Spreads", "Equity Index", -0.7),
        ("Credit Spreads", "FX EM", -0.4),
        ("Credit Spreads", "Vol Index", 0.6),
    ],
}


@dataclass(slots=True)
class TopDownConfig:
    narrative: str
    theme_weights: dict[str, float]
    severity_scale: float = 1.0
    horizon_days: int = 10
    calibration_method: str = "Historical"
    transmission_template: str = "Rate Hike"
    custom_links: list[tuple[str, str, float]] = field(default_factory=list)


def normalize_theme_weights(theme_weights: dict[str, float]) -> dict[str, float]:
    total = sum(max(0.0, v) for v in theme_weights.values())
    if total == 0:
        return {k: 0.0 for k in theme_weights}
    return {k: round(max(0.0, v) / total, 4) for k, v in theme_weights.items()}


def generate_asset_class_shocks(config: TopDownConfig) -> dict[str, dict[str, float]]:
    weights = normalize_theme_weights(config.theme_weights)
    base = {
        "Rates": {"parallel_shift_bp": 40.0, "twist_bp": 10.0, "butterfly_bp": 5.0},
        "FX": {"spot_pct": -0.04, "vol_pct": 0.2, "basis_bp": 8.0},
        "Equities": {"index_pct": -0.1, "sector_dispersion_pct": 0.05, "vol_atm_pct": 0.3},
        "Credit": {"ig_bp": 55.0, "hy_bp": 180.0, "recovery_shift_pct": -0.08},
        "Commodities": {"energy_pct": -0.06, "metals_pct": -0.04, "ag_pct": -0.03},
        "Volatility": {"vix_pts": 10.0, "move_pts": 20.0, "corr_shift": 0.2},
    }

    recession_boost = weights.get("Recession", 0.0)
    stag_boost = weights.get("Stagflation", 0.0)
    geop_boost = weights.get("Geopolitical", 0.0)

    shocks = {}
    for asset_class, params in base.items():
        adjusted: dict[str, float] = {}
        for key, value in params.items():
            multiplier = config.severity_scale * (1 + recession_boost * 0.5 + stag_boost * 0.4 + geop_boost * 0.25)
            adjusted[key] = round(value * multiplier, 6)
        shocks[asset_class] = adjusted
    return shocks


def transmission_links(config: TopDownConfig) -> pd.DataFrame:
    links = TRANSMISSION_TEMPLATES.get(config.transmission_template, []) + list(config.custom_links)
    return pd.DataFrame(links, columns=["source", "target", "weight"])


def coherence_checks(shocks: dict[str, dict[str, float]]) -> list[str]:
    warnings: list[str] = []
    eq = shocks.get("Equities", {})
    vol = shocks.get("Volatility", {})
    fx = shocks.get("FX", {})

    if eq.get("index_pct", 0) > 0 and vol.get("vix_pts", 0) > 8:
        warnings.append("Equity index up with very high VIX level increase. Add narrative justification.")
    if fx.get("spot_pct", 0) > 0.15:
        warnings.append("FX spot shock is beyond typical stress envelope. Confirm calibration source.")
    if abs(shocks.get("Rates", {}).get("parallel_shift_bp", 0)) > 500:
        warnings.append("Rates parallel shift exceeds 500bp. Review extreme plausibility assumptions.")
    return warnings


def enforce_monotonicity(shock_sets: dict[str, dict[str, dict[str, float]]]) -> dict[str, dict[str, dict[str, float]]]:
    # input: {"Moderate": {...}, "Severe": {...}, "Extreme": {...}}
    ordered = ["Moderate", "Severe", "Extreme"]
    result = {k: {ac: params.copy() for ac, params in v.items()} for k, v in shock_sets.items()}

    for i in range(1, len(ordered)):
        prev = ordered[i - 1]
        cur = ordered[i]
        if prev not in result or cur not in result:
            continue
        for ac, params in result[cur].items():
            prev_params = result[prev].get(ac, {})
            for k, val in params.items():
                prev_val = prev_params.get(k, val)
                if abs(val) < abs(prev_val):
                    params[k] = float(np.sign(val or prev_val) * abs(prev_val))

    return result
