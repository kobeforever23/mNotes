from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


SUPPORTED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json", ".parquet"}


class FileImportError(RuntimeError):
    """Raised when a file import operation fails."""


class FileImporter:
    """File importer with preview + summary utilities."""

    def load(self, path: str | Path, sheet_name: str | None = None) -> pd.DataFrame:
        file_path = Path(path)
        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            raise FileImportError(f"Unsupported file type: {file_path.suffix}")

        try:
            suffix = file_path.suffix.lower()
            if suffix == ".csv":
                return pd.read_csv(file_path)
            if suffix in {".xlsx", ".xls"}:
                return pd.read_excel(file_path, sheet_name=sheet_name or 0)
            if suffix == ".json":
                return pd.read_json(file_path)
            if suffix == ".parquet":
                return pd.read_parquet(file_path)
            raise FileImportError(f"No loader configured for {suffix}")
        except Exception as exc:
            raise FileImportError(f"Failed to load file {file_path}: {exc}") from exc

    def available_sheets(self, path: str | Path) -> list[str]:
        file_path = Path(path)
        if file_path.suffix.lower() not in {".xlsx", ".xls"}:
            return []

        with pd.ExcelFile(file_path) as xl:
            return list(xl.sheet_names)

    def preview(self, frame: pd.DataFrame, limit: int = 100) -> pd.DataFrame:
        return frame.head(limit).copy()

    def column_stats(self, frame: pd.DataFrame) -> pd.DataFrame:
        total = len(frame)
        stats: list[dict[str, Any]] = []
        for col in frame.columns:
            series = frame[col]
            dtype = str(series.dtype)
            nulls = int(series.isna().sum())
            uniques = int(series.nunique(dropna=True))
            sample = series.dropna().head(3).tolist()
            stats.append(
                {
                    "column": col,
                    "dtype": dtype,
                    "null_count": nulls,
                    "null_pct": 0.0 if total == 0 else round(nulls / total * 100, 2),
                    "unique_count": uniques,
                    "sample_values": ", ".join(str(x) for x in sample),
                }
            )
        return pd.DataFrame(stats)
