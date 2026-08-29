"""Conservative data-cleaning and duplicate utilities."""

import pandas as pd


def missing_data_report(df):
    """Return missing counts, percentages, and dtypes."""
    missing = df.isna().sum()
    return pd.DataFrame(
        {
            "missing_count": missing,
            "missing_percent": (missing / len(df) * 100).round(2),
            "dtype": df.dtypes.astype(str),
        }
    ).sort_values("missing_percent", ascending=False)


def clean_covid_data(df, numeric_columns=None, compute_active=True):
    """Apply conservative cleaning without interpreting missing as zero."""
    result = df.copy()
    numeric_columns = numeric_columns or [
        "Confirmed",
        "Deaths",
        "Recovered",
        "Active",
        "Incident_Rate",
        "Case_Fatality_Ratio",
        "Lat",
        "Long_",
    ]

    for column in numeric_columns:
        if column in result.columns:
            result[column] = pd.to_numeric(result[column], errors="coerce")
            result.loc[result[column] < 0, column] = pd.NA

    required = {"Confirmed", "Deaths", "Recovered"}
    if compute_active and required.issubset(result.columns):
        derived_active = result["Confirmed"] - result["Deaths"] - result["Recovered"]
        if "Active" in result.columns:
            result["Active"] = result["Active"].combine_first(derived_active)
        else:
            result["Active"] = derived_active

    return result


def duplicate_report(df):
    """Report exact and administrative-key duplicates for review."""
    exact_duplicates = int(df.duplicated().sum())
    keys = [
        column
        for column in ("Date", "Country_Region", "Province_State", "Admin2")
        if column in df.columns
    ]
    key_duplicates = int(df.duplicated(subset=keys, keep=False).sum()) if keys else 0
    return {
        "exact_duplicate_rows": exact_duplicates,
        "key_duplicate_rows": key_duplicates,
        "duplicate_keys": keys,
    }


def remove_exact_duplicates(df):
    """Remove only byte-for-byte equivalent records."""
    return df.drop_duplicates().reset_index(drop=True)
