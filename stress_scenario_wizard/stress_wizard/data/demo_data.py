from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
import random
from typing import Iterable

import numpy as np
import pandas as pd

from stress_wizard.models import DataBundle


ASSET_CLASSES = ["Rates", "FX", "Equities", "Credit", "Commodities", "Volatility"]
DESKS = [
    "Rates Macro",
    "Rates Exotics",
    "G10 FX",
    "EM FX",
    "Equity Derivatives",
    "Cash Equities",
    "IG Credit",
    "HY Credit",
    "Commodities",
    "Volatility Trading",
    "Structured Solutions",
    "EM Rates",
    "FX Options",
    "Prime Finance",
    "Securitized Products",
    "Municipal",
    "EM Credit",
    "Cross-Asset Vol",
    "XVA",
]
CURRENCIES = ["USD", "EUR", "GBP", "JPY", "CHF", "CAD", "AUD", "CNY"]
GEOS = ["US", "EMEA", "APAC", "LATAM"]
SECTORS = ["Tech", "Energy", "Financials", "Healthcare", "Industrials", "Utilities"]
TENORS = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]


def _rng(seed: int = 42) -> np.random.Generator:
    return np.random.default_rng(seed)


def generate_positions(n: int = 3_500, seed: int = 42) -> pd.DataFrame:
    rng = _rng(seed)
    now = datetime.now()

    positions = pd.DataFrame(
        {
            "instrument_id": [f"INS-{i:06d}" for i in range(1, n + 1)],
            "asset_class": rng.choice(ASSET_CLASSES, n),
            "sub_asset_class": rng.choice(["Macro", "Flow", "Options", "Credit", "Commod"], n),
            "desk": rng.choice(DESKS, n),
            "book": rng.choice([f"BOOK-{i:03d}" for i in range(1, 101)], n),
            "notional": rng.normal(7_500_000, 2_500_000, n).clip(250_000, 30_000_000),
            "direction": rng.choice([1, -1], n),
            "maturity": [now + timedelta(days=int(x)) for x in rng.integers(30, 3650, n)],
            "currency": rng.choice(CURRENCIES, n),
            "geography": rng.choice(GEOS, n),
        }
    )
    return positions


def generate_sensitivities(positions: pd.DataFrame, seed: int = 43) -> pd.DataFrame:
    rng = _rng(seed)
    n = len(positions)
    scale = positions["notional"].to_numpy() / 1_000_000.0

    df = pd.DataFrame(
        {
            "instrument_id": positions["instrument_id"],
            "delta": rng.normal(0.8, 0.35, n) * scale,
            "gamma": rng.normal(0.02, 0.01, n) * scale,
            "vega": rng.normal(0.1, 0.07, n) * scale,
            "rho": rng.normal(0.05, 0.04, n) * scale,
            "cs01": rng.normal(0.08, 0.03, n) * scale,
            "dv01": rng.normal(0.06, 0.02, n) * scale,
            "theta": rng.normal(-0.03, 0.02, n) * scale,
            "convexity": rng.normal(0.015, 0.008, n) * scale,
            "cross_gamma": rng.normal(0.005, 0.002, n) * scale,
        }
    )

    # Intentionally introduce sparse missing values for validation dashboard demonstration.
    missing_ix = rng.choice(n, int(n * 0.02), replace=False)
    df.loc[missing_ix, "vega"] = np.nan
    return df


def generate_risk_driver_taxonomy(n: int = 300_000, seed: int = 44) -> pd.DataFrame:
    rng = _rng(seed)
    asset_class = rng.choice(ASSET_CLASSES, n)
    sector = rng.choice(SECTORS, n)
    geography = rng.choice(GEOS, n)
    tenor = rng.choice(TENORS, n)

    df = pd.DataFrame(
        {
            "driver_id": [f"DRV-{i:07d}" for i in range(1, n + 1)],
            "name": [f"{asset_class[i]}_{sector[i]}_{geography[i]}_{tenor[i]}_{i:07d}" for i in range(n)],
            "asset_class": asset_class,
            "geography": geography,
            "tenor": tenor,
            "sector": sector,
            "issuer": rng.choice([f"Issuer-{i:05d}" for i in range(1, 5001)], n),
            "curve_point": rng.choice(["Front", "Belly", "Long"], n),
        }
    )
    return df


def generate_market_data(risk_drivers: pd.DataFrame, seed: int = 45) -> pd.DataFrame:
    rng = _rng(seed)
    n = len(risk_drivers)
    now = datetime.now()

    levels = np.where(
        risk_drivers["asset_class"].eq("Rates"),
        rng.normal(2.5, 1.0, n),
        rng.normal(100.0, 35.0, n),
    )

    as_of = np.array(
        [
            now - timedelta(days=int(x))
            for x in rng.choice([0, 1, 2, 3], size=n, p=[0.6, 0.25, 0.1, 0.05])
        ]
    )

    return pd.DataFrame(
        {
            "driver_id": risk_drivers["driver_id"],
            "asset_class": risk_drivers["asset_class"],
            "level": levels,
            "as_of": as_of,
            "source": rng.choice(["Bloomberg", "Refinitiv", "Internal"], n),
        }
    )


def generate_sample_driver_shocks(risk_drivers: pd.DataFrame, n: int = 1_000, seed: int = 46) -> pd.DataFrame:
    rng = _rng(seed)
    sample = risk_drivers.sample(n=min(n, len(risk_drivers)), random_state=seed).copy()
    sample["shock"] = rng.normal(0.0, 0.08, len(sample))
    sample["lock"] = rng.choice([True, False], len(sample), p=[0.1, 0.9])
    return sample[["driver_id", "shock", "lock"]]


def generate_demo_bundle(risk_driver_count: int = 60_000) -> DataBundle:
    # Default to 60k for instant startup; users can regenerate 300k from the UI.
    positions = generate_positions()
    sensitivities = generate_sensitivities(positions)
    risk_drivers = generate_risk_driver_taxonomy(risk_driver_count)
    market_data = generate_market_data(risk_drivers)
    return DataBundle(
        positions=positions,
        sensitivities=sensitivities,
        market_data=market_data,
        risk_drivers=risk_drivers,
    )


def write_demo_files(root: Path | str = "demo_data") -> Iterable[Path]:
    root_path = Path(root)
    root_path.mkdir(parents=True, exist_ok=True)
    bundle = generate_demo_bundle(risk_driver_count=12_000)

    outputs = []
    for name, frame in {
        "positions.csv": bundle.positions,
        "sensitivities.csv": bundle.sensitivities,
        "risk_drivers.csv": bundle.risk_drivers,
        "market_data.csv": bundle.market_data,
    }.items():
        path = root_path / name
        frame.to_csv(path, index=False)
        outputs.append(path)

    shocks = generate_sample_driver_shocks(bundle.risk_drivers)
    shock_path = root_path / "driver_shocks.csv"
    shocks.to_csv(shock_path, index=False)
    outputs.append(shock_path)
    return outputs


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    created = list(write_demo_files())
    print("Demo files written:")
    for file in created:
        print(f" - {file}")
