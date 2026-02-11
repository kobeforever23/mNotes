# Stress Scenario Generation Wizard

This folder is a complete, self-contained package for the Stress Scenario Generation Wizard.

## Start Here

1. Open terminal in this folder.
2. Create venv and install dependencies.
3. Run smoke check.
4. Launch app.

```bash
cd /Users/admin/cptCodex/stress_scenario_wizard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_smoke_check.py
python main.py
```

Or use helper scripts:

```bash
cd /Users/admin/cptCodex/stress_scenario_wizard
./scripts/setup_local_env.sh
./scripts/run_app.sh
```

## What Is In This Folder

- `main.py` - application entrypoint
- `stress_wizard/` - full source code (UI, calc, ingestion, scenario, governance, export)
- `demo_data/` - demo portfolio/risk data + governance configs
- `scripts/` - smoke check and demo generators
  - `scripts/setup_local_env.sh` - create venv and install deps
  - `scripts/run_app.sh` - launch app from local venv
- `tests/` - unit tests
- `app_settings.json` - runtime defaults
- `USER_GUIDE.md` - click-through walkthrough
- `PROJECT_STRUCTURE.md` - full folder map

## Validation Commands

```bash
python scripts/run_smoke_check.py
python -m pytest -q tests
python -m compileall main.py stress_wizard tests scripts
```

## Demo Package Generation

```bash
python scripts/generate_demo_package.py
```

This produces preview outputs under:

- `demo_data/sample_output/scenarios/...`

## Notes

- If `PySide6` is missing, GUI launch will fail until dependencies are installed.
- If `openpyxl` is missing, Excel output is skipped but CSV previews still generate.
