from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import pandas as pd

from stress_wizard.models import (
    REQUIRED_DRIVER_COLUMNS,
    REQUIRED_MARKET_COLUMNS,
    REQUIRED_POSITION_COLUMNS,
    REQUIRED_SENS_COLUMNS,
)


@dataclass(slots=True)
class ValidationIssue:
    severity: str
    category: str
    message: str
    recommendation: str


@dataclass(slots=True)
class ValidationScorecard:
    total_score: float
    coverage_positions_with_complete_greeks: float
    coverage_risk_drivers_with_market_data: float
    duplicate_count: int
    stale_market_data_count: int
    missing_required_columns: dict[str, list[str]]
    issues: list[ValidationIssue]


def _missing_columns(frame: pd.DataFrame, required: set[str]) -> list[str]:
    return sorted([col for col in required if col not in frame.columns])


def validate_bundle(
    positions: pd.DataFrame,
    sensitivities: pd.DataFrame,
    market_data: pd.DataFrame,
    risk_drivers: pd.DataFrame,
) -> ValidationScorecard:
    issues: list[ValidationIssue] = []
    missing_required: dict[str, list[str]] = {
        "positions": _missing_columns(positions, REQUIRED_POSITION_COLUMNS),
        "sensitivities": _missing_columns(sensitivities, REQUIRED_SENS_COLUMNS),
        "market_data": _missing_columns(market_data, REQUIRED_MARKET_COLUMNS),
        "risk_drivers": _missing_columns(risk_drivers, REQUIRED_DRIVER_COLUMNS),
    }

    for category, missing in missing_required.items():
        if missing:
            issues.append(
                ValidationIssue(
                    severity="HIGH",
                    category=category,
                    message=f"Missing required columns: {', '.join(missing)}",
                    recommendation="Use the column mapping assistant to map or create these fields.",
                )
            )

    merged = positions.merge(sensitivities, on="instrument_id", how="left") if "instrument_id" in positions and "instrument_id" in sensitivities else positions.copy()
    greek_cols = ["delta", "gamma", "vega", "rho", "cs01", "dv01", "theta", "convexity"]
    existing_greek_cols = [c for c in greek_cols if c in merged.columns]
    if existing_greek_cols:
        complete = (~merged[existing_greek_cols].isna()).all(axis=1)
        greek_coverage = float(complete.mean()) * 100.0 if len(merged) > 0 else 0.0
    else:
        greek_coverage = 0.0

    if "driver_id" in market_data.columns and "driver_id" in risk_drivers.columns:
        coverage = risk_drivers["driver_id"].isin(market_data["driver_id"]).mean() * 100.0
    else:
        coverage = 0.0

    duplicate_count = 0
    if "instrument_id" in positions.columns:
        duplicate_count += int(positions.duplicated(subset=["instrument_id"]).sum())
    if "driver_id" in risk_drivers.columns:
        duplicate_count += int(risk_drivers.duplicated(subset=["driver_id"]).sum())

    stale_market = 0
    if "as_of" in market_data.columns:
        as_of = pd.to_datetime(market_data["as_of"], errors="coerce")
        stale_market = int((as_of < (datetime.now() - timedelta(days=1))).sum())

    if stale_market > 0:
        issues.append(
            ValidationIssue(
                severity="MEDIUM",
                category="market_data",
                message=f"{stale_market} market data points are older than T-1.",
                recommendation="Refresh data source or document override in methodology notes.",
            )
        )

    if duplicate_count > 0:
        issues.append(
            ValidationIssue(
                severity="MEDIUM",
                category="duplicates",
                message=f"Detected {duplicate_count} duplicate IDs.",
                recommendation="Deduplicate by latest timestamp or aggregate by book/desk.",
            )
        )

    penalty = (
        len([i for i in issues if i.severity == "HIGH"]) * 15
        + len([i for i in issues if i.severity == "MEDIUM"]) * 5
        + stale_market / max(len(market_data), 1) * 30
    )

    score = max(0.0, round((greek_coverage * 0.5 + coverage * 0.5) - penalty, 2))

    return ValidationScorecard(
        total_score=score,
        coverage_positions_with_complete_greeks=round(greek_coverage, 2),
        coverage_risk_drivers_with_market_data=round(float(coverage), 2),
        duplicate_count=duplicate_count,
        stale_market_data_count=stale_market,
        missing_required_columns=missing_required,
        issues=issues,
    )
