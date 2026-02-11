from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any

import pandas as pd

from stress_wizard.models import Scenario


def scenario_folder_name(name: str, created_at: datetime) -> str:
    safe = "_".join(name.replace("/", "-").replace(" ", "_").split())
    return f"{created_at:%Y-%m-%d}_{safe}"


def ensure_root_structure(root: Path) -> None:
    for rel in [
        "scenarios",
        "templates",
        "governance",
        "market_data_cache",
        "portfolios",
    ]:
        (root / rel).mkdir(parents=True, exist_ok=True)


def create_scenario_structure(root: Path, scenario: Scenario) -> Path:
    ensure_root_structure(root)
    scenario_dir = root / "scenarios" / scenario_folder_name(scenario.metadata.name, scenario.metadata.created_at)
    charts_dir = scenario_dir / "charts"
    governance_dir = scenario_dir / "governance"
    version_dir = governance_dir / "version_history"

    for path in [scenario_dir, charts_dir, governance_dir, version_dir]:
        path.mkdir(parents=True, exist_ok=True)

    return scenario_dir


def _serialize_scenario(scenario: Scenario) -> dict[str, Any]:
    payload = {
        "metadata": {
            "scenario_id": scenario.metadata.scenario_id,
            "name": scenario.metadata.name,
            "author": scenario.metadata.author,
            "created_at": scenario.metadata.created_at.isoformat(),
            "severity": scenario.metadata.severity.value,
            "horizon_days": scenario.metadata.horizon_days,
            "approach": scenario.metadata.approach.value,
            "calibration": scenario.metadata.calibration.value,
            "as_of_date": scenario.metadata.as_of_date.isoformat(),
        },
        "narrative": {
            "text": scenario.narrative.text,
            "themes": scenario.narrative.themes,
            "transmission_links": scenario.narrative.transmission_links,
        },
        "shocks": {
            "asset_class_shocks": scenario.shocks.asset_class_shocks,
            "locked_drivers": sorted(scenario.shocks.locked_drivers),
            "risk_driver_shock_count": int(len(scenario.shocks.risk_driver_shocks)),
        },
    }
    return payload


def write_scenario_config(scenario_dir: Path, scenario: Scenario) -> Path:
    path = scenario_dir / "scenario_config.json"
    path.write_text(json.dumps(_serialize_scenario(scenario), indent=2), encoding="utf-8")
    return path


def write_driver_shocks(scenario_dir: Path, shocks: pd.DataFrame) -> Path:
    path = scenario_dir / "driver_shocks.csv"
    shocks.to_csv(path, index=False)
    return path


def write_results_workbook(scenario_dir: Path, sheets: dict[str, pd.DataFrame]) -> Path:
    path = scenario_dir / "pnl_results.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, frame in sheets.items():
            frame.to_excel(writer, sheet_name=name[:31], index=False)
    return path


def write_narrative(scenario_dir: Path, narrative: str) -> Path:
    path = scenario_dir / "narrative.md"
    path.write_text(narrative, encoding="utf-8")
    return path


def append_audit_log(scenario_dir: Path, action: str, actor: str, details: dict[str, Any] | None = None) -> Path:
    path = scenario_dir / "audit_log.json"
    payload: list[dict[str, Any]] = []
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
    payload.append(
        {
            "timestamp": datetime.now().isoformat(),
            "actor": actor,
            "action": action,
            "details": details or {},
        }
    )
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def write_governance_artifacts(
    scenario_dir: Path,
    approval_status: dict[str, Any],
    comments: list[dict[str, Any]],
    distribution_log: list[dict[str, Any]],
) -> None:
    gov_dir = scenario_dir / "governance"
    (gov_dir / "approval_status.json").write_text(json.dumps(approval_status, indent=2), encoding="utf-8")
    (gov_dir / "comments_thread.json").write_text(json.dumps(comments, indent=2), encoding="utf-8")
    (gov_dir / "distribution_log.json").write_text(json.dumps(distribution_log, indent=2), encoding="utf-8")
