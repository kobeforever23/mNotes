from __future__ import annotations

import pandas as pd

from stress_wizard.calc.engine import CalculationConfig, compute_pnl


def test_compute_pnl_outputs_required_columns() -> None:
    positions = pd.DataFrame(
        {
            "instrument_id": ["A", "B"],
            "asset_class": ["Equities", "Rates"],
            "notional": [1_000_000, 2_000_000],
            "direction": [1, -1],
            "desk": ["Eq", "Rates"],
            "book": ["B1", "B2"],
        }
    )
    sensitivities = pd.DataFrame(
        {
            "instrument_id": ["A", "B"],
            "delta": [1000.0, 800.0],
            "gamma": [50.0, 40.0],
            "vega": [200.0, 100.0],
            "rho": [10.0, 20.0],
            "cs01": [5.0, 8.0],
            "dv01": [0.0, 0.0],
            "theta": [-2.0, -4.0],
            "convexity": [1.0, 2.0],
            "cross_gamma": [0.2, 0.1],
        }
    )
    shocks = {
        "Equities": {"index_pct": -0.1, "vol_atm_pct": 0.3},
        "Rates": {"parallel_shift_bp": 120.0, "twist_bp": 10.0, "butterfly_bp": 5.0},
    }

    out = compute_pnl(positions, sensitivities, shocks, config=CalculationConfig())

    assert len(out) == 2
    assert "pnl_total" in out.columns
    assert "pnl_delta" in out.columns
    assert "pnl_gamma" in out.columns
    assert out["pnl_total"].notna().all()


def test_driver_shock_override_replaces_ds() -> None:
    positions = pd.DataFrame(
        {
            "instrument_id": ["A"],
            "asset_class": ["Equities"],
            "notional": [1_000_000],
            "direction": [1],
            "desk": ["Eq"],
            "book": ["B1"],
            "driver_id": ["DRV-1"],
        }
    )
    sensitivities = pd.DataFrame(
        {
            "instrument_id": ["A"],
            "delta": [1000.0],
            "gamma": [0.0],
            "vega": [0.0],
            "rho": [0.0],
            "cs01": [0.0],
            "dv01": [0.0],
            "theta": [0.0],
            "convexity": [0.0],
            "cross_gamma": [0.0],
        }
    )
    shocks = {"Equities": {"index_pct": -0.10, "vol_atm_pct": 0.1}}
    driver_shocks = pd.DataFrame({"driver_id": ["DRV-1"], "shock": [-0.25]})

    out = compute_pnl(positions, sensitivities, shocks, driver_shocks=driver_shocks)
    # Delta * dS = 1000 * -0.25
    assert round(float(out.iloc[0]["pnl_delta"]), 2) == -250.0
