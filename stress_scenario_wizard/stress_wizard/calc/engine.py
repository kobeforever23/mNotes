from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd


@dataclass(slots=True)
class CalculationConfig:
    horizon_days: int = 10
    correlation_regime: float = 0.35  # 0=normal, 1=crisis
    liquidity_bps: float = 12.0
    funding_spread_bps: float = 25.0


def _asset_class_move_map(asset_class_shocks: dict[str, dict[str, float]]) -> pd.DataFrame:
    rows = []
    for asset_class, values in asset_class_shocks.items():
        ds = float(
            values.get("index_pct")
            or values.get("spot_pct")
            or values.get("parallel_shift_bp", 0.0) / 10000.0
            or values.get("energy_pct", 0.0)
        )
        dvol = float(values.get("vol_pct") or values.get("vol_atm_pct") or values.get("vix_pts", 0.0) / 100.0)
        dr = float(values.get("parallel_shift_bp", 0.0) / 10000.0)
        dspread = float(values.get("ig_bp", 0.0) / 10000.0)
        rows.append(
            {
                "asset_class": asset_class,
                "dS": ds,
                "dVol": dvol,
                "dR": dr,
                "dSpread": dspread,
            }
        )
    return pd.DataFrame(rows)


def compute_pnl(
    positions: pd.DataFrame,
    sensitivities: pd.DataFrame,
    asset_class_shocks: dict[str, dict[str, float]],
    driver_shocks: pd.DataFrame | None = None,
    config: CalculationConfig | None = None,
) -> pd.DataFrame:
    """Compute stress P&L with first and second order terms.

    Required columns:
    - positions: instrument_id, asset_class, notional, direction, desk, book
    - sensitivities: instrument_id, delta, gamma, vega, rho, cs01, theta, convexity, cross_gamma
    """
    if config is None:
        config = CalculationConfig()

    merged = positions.merge(sensitivities, on="instrument_id", how="left", suffixes=("", "_sens"))
    merged = merged.fillna(0.0)

    move_map = _asset_class_move_map(asset_class_shocks)
    merged = merged.merge(move_map, on="asset_class", how="left")
    merged[["dS", "dVol", "dR", "dSpread"]] = merged[["dS", "dVol", "dR", "dSpread"]].fillna(0.0)

    if driver_shocks is not None and not driver_shocks.empty and "driver_id" in driver_shocks.columns and "driver_id" in merged.columns:
        merged = merged.merge(driver_shocks[["driver_id", "shock"]], on="driver_id", how="left")
        merged["dS"] = np.where(merged["shock"].notna(), merged["shock"], merged["dS"])

    direction = merged.get("direction", pd.Series(1.0, index=merged.index)).replace({0: 1.0})
    dt = config.horizon_days / 365.0

    merged["pnl_delta"] = merged["delta"] * merged["dS"] * direction
    merged["pnl_gamma"] = 0.5 * merged["gamma"] * np.square(merged["dS"])
    merged["pnl_vega"] = merged["vega"] * merged["dVol"]
    merged["pnl_rho"] = merged["rho"] * merged["dR"]
    merged["pnl_cs01"] = merged["cs01"] * merged["dSpread"]
    merged["pnl_theta"] = merged["theta"] * dt
    merged["pnl_convexity"] = 0.5 * merged["convexity"] * np.square(merged["dR"])

    corr = 0.15 + 0.85 * config.correlation_regime
    merged["pnl_cross_gamma"] = merged.get("cross_gamma", 0.0) * merged["dS"] * merged["dVol"] * corr

    merged["pnl_funding"] = -abs(config.funding_spread_bps / 10000.0) * merged["notional"] * 0.01
    merged["pnl_liquidity"] = -abs(config.liquidity_bps / 10000.0) * merged["notional"] * 0.015

    pnl_cols = [
        "pnl_delta",
        "pnl_gamma",
        "pnl_vega",
        "pnl_rho",
        "pnl_cs01",
        "pnl_theta",
        "pnl_convexity",
        "pnl_cross_gamma",
        "pnl_funding",
        "pnl_liquidity",
    ]

    merged["pnl_total"] = merged[pnl_cols].sum(axis=1)
    return merged


def portfolio_summary(results: pd.DataFrame) -> dict[str, Any]:
    cols = [c for c in results.columns if c.startswith("pnl_")]
    out = {c: float(results[c].sum()) for c in cols}
    out["position_count"] = int(len(results))
    out["loss_positions"] = int((results["pnl_total"] < 0).sum()) if "pnl_total" in results.columns else 0
    return out
