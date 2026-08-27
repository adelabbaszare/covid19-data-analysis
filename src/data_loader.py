"""Data loading and schema inspection utilities."""
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

def discover_csv_files(data_dir):
    path = Path(data_dir)
    if not path.exists():
        raise FileNotFoundError(f"Data directory does not exist: {path}")
    files = sorted(path.glob("*.csv"))
    if not files:
        raise FileNotFoundError(f"No CSV files found in: {path}")
    return files

def inspect_schema(files):
    files = [Path(file) for file in files]
    if not files:
        raise ValueError("At least one CSV file is required.")
    files_by_column = {}
    column_dtypes = {}
    for file in files:
        sample = pd.read_csv(file, nrows=100)
        for column, dtype in sample.dtypes.items():
            files_by_column.setdefault(column, []).append(file.name)
            column_dtypes.setdefault(column, set()).add(str(dtype))
    return {
        "file_count": len(files),
        "columns": sorted(files_by_column),
        "files_by_column": {k: sorted(v) for k, v in files_by_column.items()},
        "column_dtypes": {k: sorted(v) for k, v in column_dtypes.items()},
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
    if "Last_Update" in result.columns:
        result["Last_Update"] = pd.to_datetime(result["Last_Update"], errors="coerce")
    return result

def load_covid_data(data_dir):
    frames = []
    for file in discover_csv_files(data_dir):
        frame = standardize_schema(pd.read_csv(file))
        frame["Source_File"] = file.name
        frames.append(frame)
    return pd.concat(frames, ignore_index=True, sort=False)

def missing_data_report(df):
    missing = df.isna().sum()
    return pd.DataFrame({
        "missing_count": missing,
        "missing_percent": (missing / len(df) * 100).round(2),
        "dtype": df.dtypes.astype(str),
    }).sort_values("missing_percent", ascending=False)
