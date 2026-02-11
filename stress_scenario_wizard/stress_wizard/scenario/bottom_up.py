from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(slots=True)
class PropagationRule:
    level: str  # Asset Class | Sector | Issuer | Tenor
    key: str
    multiplier: float


def search_risk_drivers(risk_drivers: pd.DataFrame, query: str, limit: int = 5000) -> pd.DataFrame:
    if not query.strip():
        return risk_drivers.head(limit).copy()

    mask = (
        risk_drivers["driver_id"].str.contains(query, case=False, na=False)
        | risk_drivers["name"].str.contains(query, case=False, na=False)
        | risk_drivers["asset_class"].str.contains(query, case=False, na=False)
        | risk_drivers["geography"].str.contains(query, case=False, na=False)
        | risk_drivers["tenor"].str.contains(query, case=False, na=False)
        | risk_drivers.get("desk", pd.Series([""] * len(risk_drivers))).astype(str).str.contains(query, case=False, na=False)
    )
    return risk_drivers.loc[mask].head(limit).copy()


def apply_bulk_shock(shock_table: pd.DataFrame, driver_ids: list[str], shock: float) -> pd.DataFrame:
    out = shock_table.copy()
    out.loc[out["driver_id"].isin(driver_ids), "shock"] = shock
    return out


def hierarchical_propagation(
    risk_drivers: pd.DataFrame,
    parent_filters: dict[str, str],
    parent_shock: float,
    decay: float = 0.95,
    sector_multipliers: dict[str, float] | None = None,
) -> pd.DataFrame:
    sector_multipliers = sector_multipliers or {}
    mask = pd.Series(True, index=risk_drivers.index)
    for col, value in parent_filters.items():
        if col in risk_drivers.columns:
            mask &= risk_drivers[col].astype(str).str.contains(value, case=False, na=False)

    impacted = risk_drivers.loc[mask].copy()
    if impacted.empty:
        return pd.DataFrame(columns=["driver_id", "shock", "method"])

    # Example propagation logic: maturity bucket and sector multiplier.
    tenor_decay = {
        "1M": 1.00,
        "3M": 0.98,
        "6M": 0.96,
        "1Y": 0.94,
        "2Y": 0.92,
        "3Y": 0.90,
        "5Y": 0.88,
        "7Y": 0.86,
        "10Y": 0.84,
        "20Y": 0.80,
        "30Y": 0.76,
    }

    shocks = []
    for _, row in impacted.iterrows():
        tenor_mult = tenor_decay.get(str(row.get("tenor", "5Y")), decay)
        sector_mult = sector_multipliers.get(str(row.get("sector", "")), 1.0)
        shocks.append(parent_shock * tenor_mult * sector_mult)

    impacted["shock"] = np.array(shocks)
    impacted["method"] = "hierarchical"
    return impacted[["driver_id", "shock", "method"]]


def beta_propagation(
    benchmark_shocks: pd.DataFrame,
    beta_map: pd.DataFrame,
    default_beta: float = 1.0,
) -> pd.DataFrame:
    """Apply benchmark shock * beta to children.

    `benchmark_shocks` columns: benchmark_id, shock
    `beta_map` columns: driver_id, benchmark_id, beta
    """
    merged = beta_map.merge(benchmark_shocks, on="benchmark_id", how="left")
    merged["beta"] = merged["beta"].fillna(default_beta)
    merged["shock"] = merged["shock"].fillna(0.0) * merged["beta"]
    return merged[["driver_id", "shock"]]
