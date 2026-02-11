from __future__ import annotations

import pandas as pd


def _aggregate(results: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    grouped = (
        results.groupby(group_cols, dropna=False, as_index=False)
        .agg(
            pnl=("pnl_total", "sum"),
            pnl_delta=("pnl_delta", "sum"),
            pnl_gamma=("pnl_gamma", "sum"),
            pnl_vega=("pnl_vega", "sum"),
            pnl_rho=("pnl_rho", "sum"),
            pnl_cs01=("pnl_cs01", "sum"),
            pnl_theta=("pnl_theta", "sum"),
            pnl_convexity=("pnl_convexity", "sum"),
            pnl_cross_gamma=("pnl_cross_gamma", "sum"),
            pnl_funding=("pnl_funding", "sum"),
            pnl_liquidity=("pnl_liquidity", "sum"),
            position_count=("instrument_id", "count"),
        )
    )
    total = grouped["pnl"].sum()
    grouped["pct_total"] = 0.0 if abs(total) < 1e-9 else grouped["pnl"] / total * 100.0
    grouped["rank"] = grouped["pnl"].rank(method="dense", ascending=True).astype(int)
    grouped = grouped.sort_values("pnl")
    return grouped


def by_asset_class(results: pd.DataFrame) -> pd.DataFrame:
    return _aggregate(results, ["asset_class"])


def by_risk_factor(results: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for factor, col in {
        "Delta": "pnl_delta",
        "Gamma": "pnl_gamma",
        "Vega": "pnl_vega",
        "Rho": "pnl_rho",
        "CS01": "pnl_cs01",
        "Theta": "pnl_theta",
        "Convexity": "pnl_convexity",
        "CrossGamma": "pnl_cross_gamma",
        "Funding": "pnl_funding",
        "Liquidity": "pnl_liquidity",
    }.items():
        rows.append({"risk_factor": factor, "pnl": float(results[col].sum())})
    out = pd.DataFrame(rows).sort_values("pnl")
    total = out["pnl"].sum()
    out["pct_total"] = 0.0 if abs(total) < 1e-9 else out["pnl"] / total * 100.0
    out["rank"] = out["pnl"].rank(method="dense", ascending=True).astype(int)
    return out


def by_desk(results: pd.DataFrame) -> pd.DataFrame:
    return _aggregate(results, ["desk"])


def by_book(results: pd.DataFrame) -> pd.DataFrame:
    return _aggregate(results, ["desk", "book"])


def by_position(results: pd.DataFrame) -> pd.DataFrame:
    return _aggregate(results, ["instrument_id", "desk", "book", "asset_class"]) 


def by_geography(results: pd.DataFrame) -> pd.DataFrame:
    if "geography" not in results.columns:
        tmp = results.copy()
        tmp["geography"] = "Unknown"
        return _aggregate(tmp, ["geography"])
    return _aggregate(results, ["geography"])


def by_tenor_bucket(results: pd.DataFrame) -> pd.DataFrame:
    if "tenor" not in results.columns:
        tmp = results.copy()
        tmp["tenor"] = "N/A"
        return _aggregate(tmp, ["tenor"])
    return _aggregate(results, ["tenor"])
