"""Data loading, cleaning, and time-series analysis utilities."""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

COLUMN_ALIASES = {
    "Province/State": "Province_State",
    "Country/Region": "Country_Region",
    "Last Update": "Last_Update",
    "Latitude": "Lat",
    "Longitude": "Long_",
    "Incidence_Rate": "Incident_Rate",
    "Case-Fatality_Ratio": "Case_Fatality_Ratio",
}

NUMERIC_COLUMNS = [
    "Confirmed",
    "Deaths",
    "Recovered",
    "Active",
    "Incident_Rate",
    "Case_Fatality_Ratio",
    "Lat",
    "Long_",
]

DATE_COLUMN_CANDIDATES = ["Date", "Last_Update"]


def discover_csv_files(data_dir):
    path = Path(data_dir)
    if not path.exists():
        raise FileNotFoundError(f"Data directory does not exist: {path}")
    files = sorted(path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in: {path}")
    return files


def extract_date_from_filename(file_path):
    """Extract a report date from common JHU-style CSV file names."""
    stem = Path(file_path).stem

    for fmt in ("%m-%d-%Y", "%m-%d-%y", "%Y-%m-%d", "%Y_%m_%d"):
        parsed = pd.to_datetime(stem, format=fmt, errors="coerce")
        if not pd.isna(parsed):
            return parsed.normalize()

    match = re.search(r"(\d{4})[-_](\d{1,2})[-_](\d{1,2})", stem)
    if match:
        parsed = pd.to_datetime("-".join(match.groups()), errors="coerce")
        if not pd.isna(parsed):
            return parsed.normalize()

    return pd.NaT


def inspect_schema(files):
    files = [Path(file) for file in files]
    if not files:
        raise ValueError("At least one CSV file is required.")

    files_by_column, column_dtypes, dates_from_filenames = {}, {}, {}

    for file in files:
        sample = pd.read_csv(file, nrows=100)
        dates_from_filenames[file.name] = extract_date_from_filename(file)
        for column, dtype in sample.dtypes.items():
            files_by_column.setdefault(column, []).append(file.name)
            column_dtypes.setdefault(column, set()).add(str(dtype))

    return {
        "file_count": len(files),
        "columns": sorted(files_by_column),
        "files_by_column": {k: sorted(v) for k, v in files_by_column.items()},
        "column_dtypes": {k: sorted(v) for k, v in column_dtypes.items()},
        "dates_from_filenames": dates_from_filenames,
    }


def _coalesce_columns(df, target, alias):
    if alias not in df.columns:
        return df
    if target in df.columns:
        df[target] = df[target].combine_first(df[alias])
        return df.drop(columns=alias)
    return df.rename(columns={alias: target})


def standardize_schema(df):
    result = df.copy()
    for alias, canonical in COLUMN_ALIASES.items():
        result = _coalesce_columns(result, canonical, alias)

    for column in NUMERIC_COLUMNS:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce")

    if "Last_Update" in result.columns:
        result["Last_Update"] = pd.to_datetime(
            result["Last_Update"], errors="coerce", utc=True
        ).dt.tz_localize(None)

    return result


def load_covid_data(data_dir):
    """Load reports, standardize schemas, and attach the report date."""
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


def missing_data_report(df):
    missing = df.isna().sum()
    return pd.DataFrame({
        "missing_count": missing,
        "missing_percent": (missing / len(df) * 100).round(2),
        "dtype": df.dtypes.astype(str),
    }).sort_values("missing_percent", ascending=False)


def clean_covid_data(df, compute_active=True):
    """Apply conservative cleaning without treating unknown values as zero."""
    result = df.copy()

    for column in NUMERIC_COLUMNS:
        if column in result.columns:
            result.loc[result[column] < 0, column] = pd.NA

    if compute_active and {"Confirmed", "Deaths", "Recovered"}.issubset(result.columns):
        derived_active = result["Confirmed"] - result["Deaths"] - result["Recovered"]
        if "Active" not in result.columns:
            result["Active"] = derived_active
        else:
            result["Active"] = result["Active"].combine_first(derived_active)

    return result


def duplicate_report(df):
    """Report exact and key-based duplicate records."""
    exact_duplicates = int(df.duplicated().sum())
    keys = [column for column in ["Date", "Country_Region", "Province_State", "Admin2"] if column in df.columns]

    key_duplicates = 0
    if keys:
        key_duplicates = int(df.duplicated(subset=keys, keep=False).sum())

    return {
        "exact_duplicate_rows": exact_duplicates,
        "key_duplicate_rows": key_duplicates,
        "duplicate_keys": keys,
    }


def remove_exact_duplicates(df):
    return df.drop_duplicates().reset_index(drop=True)


def aggregate_country_daily(df):
    """Aggregate regional records into one record per country and report date."""
    required = {"Date", "Country_Region"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    metrics = [column for column in ["Confirmed", "Deaths", "Recovered", "Active"] if column in df.columns]
    if not metrics:
        raise ValueError("No epidemiological metric columns are available.")

    data = df.dropna(subset=["Date", "Country_Region"]).copy()
    return (
        data.groupby(["Date", "Country_Region"], as_index=False)[metrics]
        .sum(min_count=1)
        .sort_values(["Country_Region", "Date"])
        .reset_index(drop=True)
    )


def add_daily_changes(country_daily):
    """Calculate daily changes from cumulative country-level metrics."""
    result = country_daily.copy().sort_values(["Country_Region", "Date"])

    metrics = [column for column in ["Confirmed", "Deaths", "Recovered", "Active"] if column in result.columns]
    for column in metrics:
        change_column = f"New_{column}"
        result[change_column] = result.groupby("Country_Region")[column].diff()
        result[change_column] = result[change_column].clip(lower=0)

    return result.reset_index(drop=True)


def get_latest_country_data(df):
    """Return the latest available country-level totals for each country."""
    country_daily = aggregate_country_daily(df)
    latest_dates = country_daily.groupby("Country_Region")["Date"].transform("max")
    return (
        country_daily[country_daily["Date"].eq(latest_dates)]
        .sort_values(["Date", "Confirmed", "Country_Region"], ascending=[False, False, True])
        .reset_index(drop=True)
    )
