# User Guide

## 1) Setup

```bash
cd /Users/admin/cptCodex/stress_scenario_wizard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_smoke_check.py
python main.py
```

## 2) Included Demo Assets

- `demo_data/positions.csv`
- `demo_data/sensitivities.csv`
- `demo_data/risk_drivers.csv`
- `demo_data/market_data.csv`
- `demo_data/driver_shocks.csv`
- `demo_data/governance/distribution_lists.json`
- `demo_data/governance/approval_rules.json`

## 3) Click-Through Demo (End-to-End)

1. App opens with a preloaded `Demo Stress Scenario`.
2. Go to `1) Ingestion`.
3. Load each demo CSV into matching category and click `Run Validation`.
4. Go to `2) Scenario Design`.
5. Click `AI Narrative (Template)`.
6. Click `Apply Top-Down Configuration`.
7. Search a theme in bottom-up section (example: `Tech`), select rows, apply bulk shock.
8. Click `Blend Into Driver Shocks`.
9. Go to `3) Calculation` and click `Run Stress Calculation`.
10. Review attribution views by desk/book/position/risk factor.
11. Go to `4) Dashboard` and inspect heatmap/waterfall/tornado/curve/correlation/coverage.
12. In `Governance Panel`, click `Submit For Review`.
13. Approve using sample reviewer email(s).
14. Click `Publish`.
15. Use `File -> Save` and `File -> Export Package`.

## 4) Output Artifacts

Saved scenario folders include:

- `scenario_config.json`
- `driver_shocks.csv`
- `pnl_results.xlsx` (if `openpyxl` installed)
- `narrative.md`
- `audit_log.json`
- `governance/approval_status.json`
- `governance/comments_thread.json`
- `governance/distribution_log.json`
- Export files: PDF/PPTX/CSV/Parquet (when export is run)

## 5) Generate Prebuilt Demo Output

```bash
python scripts/generate_demo_package.py
```

Generated under:

- `demo_data/sample_output/scenarios/...`

## 6) Operational Checks

```bash
python scripts/run_smoke_check.py
python -m pytest -q tests
```

## 7) Troubleshooting

1. `No module named PySide6`:
   - Run `pip install -r requirements.txt`.
2. `No module named pytest`:
   - Reinstall requirements.
3. Excel output missing:
   - Install `openpyxl` (already listed in requirements).
4. Export blocked:
   - Ensure governance state is `Approved` when mandatory approval is enabled.
