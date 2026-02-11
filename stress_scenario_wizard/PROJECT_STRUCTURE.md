# Project Structure

## Root

- `main.py`
- `requirements.txt`
- `app_settings.json`
- `README.md`
- `USER_GUIDE.md`
- `PROJECT_STRUCTURE.md`

## Source Code

- `stress_wizard/`
- `stress_wizard/config.py`
- `stress_wizard/models.py`
- `stress_wizard/app_state.py`
- `stress_wizard/calc/`
- `stress_wizard/ingestion/`
- `stress_wizard/scenario/`
- `stress_wizard/governance/`
- `stress_wizard/exporter/`
- `stress_wizard/ui/`

## Scripts

- `scripts/run_smoke_check.py`
- `scripts/generate_demo_package.py`
- `scripts/generate_stress_wizard_demo_data.py`
- `scripts/setup_local_env.sh`
- `scripts/run_app.sh`

## Demo Inputs

- `demo_data/positions.csv`
- `demo_data/sensitivities.csv`
- `demo_data/risk_drivers.csv`
- `demo_data/market_data.csv`
- `demo_data/driver_shocks.csv`
- `demo_data/governance/distribution_lists.json`
- `demo_data/governance/approval_rules.json`

## Demo Outputs

- `demo_data/sample_output/scenarios/...`

## Tests

- `tests/test_calc_engine.py`
- `tests/test_governance_workflow.py`
