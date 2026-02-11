from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main() -> int:
    report: dict[str, str] = {}

    try:
        import pandas as pd  # noqa: F401
        import numpy as np  # noqa: F401
        report["python_core"] = "OK"
    except Exception as exc:
        report["python_core"] = f"FAIL: {exc}"

    try:
        import plotly  # noqa: F401
        report["plotly"] = "OK"
    except Exception as exc:
        report["plotly"] = f"FAIL: {exc}"

    try:
        import PySide6  # noqa: F401
        report["pyside6"] = "OK"
    except Exception as exc:
        report["pyside6"] = f"FAIL: {exc}"

    try:
        from datetime import datetime, timedelta

        from stress_wizard.app_state import AppState
        from stress_wizard.governance.models import ApprovalRequest, ApprovalRule, ReviewerAssignment, ReviewerRole
        from stress_wizard.governance.workflow import GovernanceWorkflow

        state = AppState()
        scenario = state.ensure_scenario()
        outputs = state.run_calculation()

        if outputs.results.empty:
            raise RuntimeError("Calculation returned empty results")

        tmp_root = Path(tempfile.mkdtemp(prefix="stress_wizard_smoke_"))
        wf = GovernanceWorkflow(tmp_root)
        wf.init_state("SCN-SMOKE", actor="smoke")
        req = ApprovalRequest(
            scenario_id="SCN-SMOKE",
            scenario_name=scenario.metadata.name,
            submitted_by="smoke",
            submitted_at=datetime.now(),
            deadline=datetime.now() + timedelta(hours=4),
            cover_note="smoke",
            rule=ApprovalRule.UNANIMOUS,
            reviewers=[
                ReviewerAssignment(name="A", email="a@bank.com", role=ReviewerRole.APPROVER, sequence=1),
                ReviewerAssignment(name="B", email="b@bank.com", role=ReviewerRole.APPROVER, sequence=2),
            ],
        )
        wf.submit_for_review("SCN-SMOKE", actor="smoke", request=req)
        wf.approve("SCN-SMOKE", actor="a@bank.com", reviewer_email="a@bank.com")
        final = wf.approve("SCN-SMOKE", actor="b@bank.com", reviewer_email="b@bank.com")

        if final.get("state") != "Approved":
            raise RuntimeError("Governance flow did not reach Approved")

        report["calc_and_governance"] = "OK"
    except Exception as exc:
        report["calc_and_governance"] = f"FAIL: {exc}"

    demo_files = [
        PROJECT_ROOT / "demo_data" / "positions.csv",
        PROJECT_ROOT / "demo_data" / "sensitivities.csv",
        PROJECT_ROOT / "demo_data" / "risk_drivers.csv",
        PROJECT_ROOT / "demo_data" / "market_data.csv",
        PROJECT_ROOT / "demo_data" / "driver_shocks.csv",
        PROJECT_ROOT / "demo_data" / "governance" / "distribution_lists.json",
        PROJECT_ROOT / "demo_data" / "governance" / "approval_rules.json",
    ]
    missing = [str(p) for p in demo_files if not p.exists()]
    report["demo_files"] = "OK" if not missing else f"FAIL: missing {missing}"

    out_path = PROJECT_ROOT / "smoke_check_report.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"report_path={out_path}")

    failed = [k for k, v in report.items() if not v.startswith("OK")]
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
