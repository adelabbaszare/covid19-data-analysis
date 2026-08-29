"""Schema discovery and normalization for historical COVID-19 reports."""
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

NUMERIC_COLUMNS = (
    "Confirmed", "Deaths", "Recovered", "Active",
    "Incident_Rate", "Case_Fatality_Ratio", "Lat", "Long_",
)


def extract_date_from_filename(file_path):
    """Extract a report date from common historical filename formats."""
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


def _coalesce_columns(df, target, alias):
    if alias not in df.columns:
        return df
    if target in df.columns:
        df[target] = df[target].combine_first(df[alias])
        return df.drop(columns=alias)
    return df.rename(columns={alias: target})


def standardize_schema(df):
    """Normalize historical aliases, numeric types, and Last_Update."""
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


def inspect_schema(files):
    """Inspect source columns and data types without loading full files."""
    files = [Path(file) for file in files]
    if not files:
        raise ValueError("At least one CSV file is required.")
    files_by_column, column_dtypes, dates = {}, {}, {}
    for file in files:
        sample = pd.read_csv(file, nrows=100)
        dates[file.name] = extract_date_from_filename(file)
        for column, dtype in sample.dtypes.items():
            files_by_column.setdefault(column, []).append(file.name)
            column_dtypes.setdefault(column, set()).add(str(dtype))
    return {
        "file_count": len(files),
        "columns": sorted(files_by_column),
        "files_by_column": {k: sorted(v) for k, v in files_by_column.items()},
        "column_dtypes": {k: sorted(v) for k, v in column_dtypes.items()},
        "dates_from_filenames": dates,
    }
