from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from stress_wizard.app_state import AppState
from stress_wizard.exporter.persistence import create_scenario_structure, write_driver_shocks, write_narrative, write_scenario_config
from stress_wizard.exporter.reporting import build_narrative_document


def main() -> int:
    state = AppState()
    scenario = state.ensure_scenario()
    outputs = state.run_calculation()

    root = PROJECT_ROOT / "demo_data" / "sample_output"
    scenario_dir = create_scenario_structure(root, scenario)

    write_scenario_config(scenario_dir, scenario)
    write_driver_shocks(scenario_dir, scenario.shocks.risk_driver_shocks)

    narrative = build_narrative_document(
        scenario_name=scenario.metadata.name,
        economic_rationale="Demo package generated from built-in scenario state.",
        transmission_logic="Top-down asset shocks blended with bottom-up driver overrides.",
        calibration_method=scenario.metadata.calibration.value,
        assumptions=["Taylor expansion used for fast stress approximation"],
        limitations=["Demo package may use sampled result previews for portability"],
    )
    write_narrative(scenario_dir, narrative)

    pd.DataFrame([outputs.summary]).to_csv(scenario_dir / "summary.csv", index=False)
    outputs.attribution["asset_class"].to_csv(scenario_dir / "by_asset_class.csv", index=False)
    outputs.attribution["desk"].to_csv(scenario_dir / "by_desk.csv", index=False)
    outputs.attribution["position"].head(20000).to_csv(scenario_dir / "by_position_preview.csv", index=False)
    outputs.sensitivity.head(5000).to_csv(scenario_dir / "shift_sensitivity_preview.csv", index=False)
    outputs.results.head(50000).to_csv(scenario_dir / "position_results_preview.csv", index=False)

    try:
        with pd.ExcelWriter(scenario_dir / "pnl_results.xlsx", engine="openpyxl") as writer:
            pd.DataFrame([outputs.summary]).to_excel(writer, sheet_name="summary", index=False)
            outputs.attribution["asset_class"].to_excel(writer, sheet_name="by_asset_class", index=False)
            outputs.attribution["desk"].to_excel(writer, sheet_name="by_desk", index=False)
            outputs.attribution["position"].head(20000).to_excel(writer, sheet_name="by_position", index=False)
        xlsx_status = "created"
    except Exception:
        xlsx_status = "skipped (openpyxl missing)"

    print(f"Demo package generated: {scenario_dir}")
    print(f"XLSX status: {xlsx_status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
