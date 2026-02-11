from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from stress_wizard.calc.engine import CalculationConfig, compute_pnl


@dataclass(slots=True)
class TornadoItem:
    parameter: str
    pnl_impact: float


def sensitivity_table(
    positions: pd.DataFrame,
    sensitivities: pd.DataFrame,
    asset_class_shocks: dict[str, dict[str, float]],
    perturbations: list[float] | None = None,
) -> pd.DataFrame:
    perturbations = perturbations or [-0.25, -0.1, -0.05, 0.01, 0.05, 0.1, 0.25]

    rows = []
    base = compute_pnl(positions, sensitivities, asset_class_shocks)
    base_pnl = float(base["pnl_total"].sum())

    for ac, params in asset_class_shocks.items():
        for key in params:
            for p in perturbations:
                bumped = {k: v.copy() for k, v in asset_class_shocks.items()}
                bumped[ac][key] = params[key] * (1 + p)
                res = compute_pnl(positions, sensitivities, bumped)
                pnl = float(res["pnl_total"].sum())
                rows.append(
                    {
                        "parameter": f"{ac}.{key}",
                        "perturbation": p,
                        "pnl": pnl,
                        "delta_vs_base": pnl - base_pnl,
                    }
                )

    return pd.DataFrame(rows)


def tornado_data(sensitivity_df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        sensitivity_df.groupby("parameter", as_index=False)
        .agg(max_abs_impact=("delta_vs_base", lambda s: float(np.max(np.abs(s)))))
        .sort_values("max_abs_impact", ascending=False)
    )
    return grouped


def break_even_shift(
    positions: pd.DataFrame,
    sensitivities: pd.DataFrame,
    asset_class_shocks: dict[str, dict[str, float]],
    target_pnl: float = 0.0,
    parameter: tuple[str, str] = ("Equities", "index_pct"),
    search_range: tuple[float, float] = (-0.5, 0.5),
) -> float:
    ac, key = parameter
    low, high = search_range
    best = low
    best_diff = float("inf")

    for x in np.linspace(low, high, 300):
        candidate = {k: v.copy() for k, v in asset_class_shocks.items()}
        if ac not in candidate:
            continue
        candidate[ac][key] = x
        pnl = float(compute_pnl(positions, sensitivities, candidate, config=CalculationConfig()).get("pnl_total", pd.Series(dtype=float)).sum())
        diff = abs(pnl - target_pnl)
        if diff < best_diff:
            best = float(x)
            best_diff = diff

    return best


def marginal_contribution(results: pd.DataFrame) -> pd.DataFrame:
    total = float(results["pnl_total"].sum())
    rows = []
    for _, row in results.iterrows():
        without = total - float(row["pnl_total"])
        rows.append(
            {
                "instrument_id": row["instrument_id"],
                "desk": row.get("desk", ""),
                "book": row.get("book", ""),
                "marginal_contribution": total - without,
                "total_pnl": total,
            }
        )
    out = pd.DataFrame(rows)
    out = out.sort_values("marginal_contribution")
    return out
