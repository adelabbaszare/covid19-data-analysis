"""Reusable country-level and time-series analysis functions."""

import pandas as pd


def aggregate_country_daily(df):
    """Aggregate administrative records into one row per country and date."""
    required = {"Date", "Country_Region"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    metrics = [
        column
        for column in ("Confirmed", "Deaths", "Recovered", "Active")
        if column in df.columns
    ]
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
    """Calculate non-negative day-over-day changes for cumulative metrics."""
    result = country_daily.copy().sort_values(["Country_Region", "Date"])
    metrics = [
        column
        for column in ("Confirmed", "Deaths", "Recovered", "Active")
        if column in result.columns
    ]
    for column in metrics:
        result[f"New_{column}"] = (
            result.groupby("Country_Region")[column].diff().clip(lower=0)
        )
    return result.reset_index(drop=True)


def get_latest_country_data(df):
    """Return latest country-level totals independently per country."""
    country_daily = aggregate_country_daily(df)
    latest_dates = country_daily.groupby("Country_Region")["Date"].transform("max")
    return (
        country_daily[country_daily["Date"].eq(latest_dates)]
        .sort_values(
            ["Date", "Confirmed", "Country_Region"],
            ascending=[False, False, True],
        )
        .reset_index(drop=True)
    )


def global_daily_totals(country_daily):
    """Aggregate country-level data into one global row per date."""
    metrics = [
        column
        for column in ("Confirmed", "Deaths", "Recovered", "Active")
        if column in country_daily.columns
    ]
    return (
        country_daily.groupby("Date", as_index=False)[metrics]
        .sum(min_count=1)
        .sort_values("Date")
    )
