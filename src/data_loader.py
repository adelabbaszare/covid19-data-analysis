"""CSV discovery and loading facade.

Implementation details live in the specialized schema, cleaning, and analysis
modules. This facade keeps the notebook imports stable while reducing coupling.
"""
from pathlib import Path

import pandas as pd

from .analysis import (
    add_daily_changes,
    aggregate_country_daily,
    get_latest_country_data,
    global_daily_totals,
)
from .cleaning import (
    clean_covid_data,
    duplicate_report,
    missing_data_report,
    remove_exact_duplicates,
)
from .schema import extract_date_from_filename, inspect_schema, standardize_schema


# Re-exported for backwards compatibility with the notebook.
__all__ = [
    "discover_csv_files",
    "extract_date_from_filename",
    "inspect_schema",
    "standardize_schema",
    "load_covid_data",
    "missing_data_report",
    "clean_covid_data",
    "duplicate_report",
    "remove_exact_duplicates",
    "aggregate_country_daily",
    "add_daily_changes",
    "get_latest_country_data",
    "global_daily_totals",
]


def discover_csv_files(data_dir):
    """Return CSV files in deterministic order."""
    path = Path(data_dir)
    if not path.exists():
        raise FileNotFoundError(f"Data directory does not exist: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Expected a directory: {path}")
    files = sorted(path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in: {path}")
    return files


def load_covid_data(data_dir):
    """Load, normalize, and concatenate all COVID-19 CSV reports."""
    frames = []
    for file in discover_csv_files(data_dir):
        frame = standardize_schema(pd.read_csv(file))
        frame["Source_File"] = file.name
        frame["Date"] = extract_date_from_filename(file)
        if frame["Date"].isna().all() and "Last_Update" in frame.columns:
            frame["Date"] = frame["Last_Update"].dt.normalize()
        frames.append(frame)

    result = pd.concat(frames, ignore_index=True, sort=False)
    return result.sort_values(["Date", "Country_Region"], na_position="last").reset_index(drop=True)
