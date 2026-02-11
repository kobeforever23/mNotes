from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class ReconciliationResult:
    top_down_expected_pnl: float
    bottom_up_aggregated_pnl: float
    discrepancy: float
    discrepancy_pct: float
    narrative_consistency: str


def reconcile_top_down_bottom_up(
    top_down_attribution: pd.DataFrame,
    bottom_up_results: pd.DataFrame,
) -> ReconciliationResult:
    top_down_pnl = float(top_down_attribution.get("pnl", pd.Series(dtype=float)).sum())
    bottom_up_pnl = float(bottom_up_results.get("pnl", pd.Series(dtype=float)).sum())
    discrepancy = bottom_up_pnl - top_down_pnl
    discrepancy_pct = 0.0 if abs(top_down_pnl) < 1e-9 else (discrepancy / top_down_pnl) * 100.0

    if abs(discrepancy_pct) < 5:
        narrative = "Driver-level shocks are consistent with top-down expectations."
    elif abs(discrepancy_pct) < 15:
        narrative = "Moderate mismatch. Review propagation multipliers and locked shocks."
    else:
        narrative = "Significant mismatch detected. Revisit macro transmission and bottom-up overrides."

    return ReconciliationResult(
        top_down_expected_pnl=round(top_down_pnl, 2),
        bottom_up_aggregated_pnl=round(bottom_up_pnl, 2),
        discrepancy=round(discrepancy, 2),
        discrepancy_pct=round(discrepancy_pct, 2),
        narrative_consistency=narrative,
    )


def blend_shocks(
    top_down_shocks: pd.DataFrame,
    bottom_up_shocks: pd.DataFrame,
    weight_top_down: float,
) -> pd.DataFrame:
    weight_top_down = min(1.0, max(0.0, weight_top_down))
    merged = top_down_shocks.merge(bottom_up_shocks, on="driver_id", how="outer", suffixes=("_top", "_bottom"))
    merged["shock_top"] = merged["shock_top"].fillna(0.0)
    merged["shock_bottom"] = merged["shock_bottom"].fillna(0.0)
    merged["shock"] = merged["shock_top"] * weight_top_down + merged["shock_bottom"] * (1 - weight_top_down)
    return merged[["driver_id", "shock"]]
