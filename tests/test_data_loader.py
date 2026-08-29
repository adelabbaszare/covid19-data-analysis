import pandas as pd
import pytest

from src.analysis import add_daily_changes, aggregate_country_daily, get_latest_country_data
from src.cleaning import clean_covid_data, duplicate_report, remove_exact_duplicates
from src.data_loader import discover_csv_files, load_covid_data
from src.schema import extract_date_from_filename, standardize_schema


def test_standardize_schema_merges_historical_column_names():
    df = pd.DataFrame({
        "Country_Region": ["A", None],
        "Country/Region": [None, "B"],
        "Province/State": ["P1", "P2"],
        "Latitude": [10.0, 20.0],
        "Last Update": ["2021-01-01 01:00:00", "2021-01-02 01:00:00"],
    })
    result = standardize_schema(df)
    assert "Country/Region" not in result.columns
    assert result["Country_Region"].tolist() == ["A", "B"]
    assert result["Province_State"].tolist() == ["P1", "P2"]
    assert result["Lat"].tolist() == [10.0, 20.0]
    assert pd.api.types.is_datetime64_any_dtype(result["Last_Update"])


def test_extract_date_from_filename():
    assert str(extract_date_from_filename("01-02-2021.csv").date()) == "2021-01-02"
    assert str(extract_date_from_filename("2021-01-03.csv").date()) == "2021-01-03"
    assert pd.isna(extract_date_from_filename("unknown.csv"))


def test_discover_and_load_csv_files(tmp_path):
    data = pd.DataFrame({"Country_Region": ["A"], "Confirmed": [10]})
    data.to_csv(tmp_path / "01-02-2021.csv", index=False)
    files = discover_csv_files(tmp_path)
    assert len(files) == 1
    result = load_covid_data(tmp_path)
    assert result.loc[0, "Source_File"] == "01-02-2021.csv"
    assert result.loc[0, "Date"] == pd.Timestamp("2021-01-02")


def test_empty_data_directory_is_rejected(tmp_path):
    with pytest.raises(FileNotFoundError):
        discover_csv_files(tmp_path)


def test_cleaning_and_duplicate_policy():
    df = pd.DataFrame({
        "Confirmed": [10, -1, 15],
        "Deaths": [1, 1, 2],
        "Recovered": [5, 2, 10],
        "Active": [pd.NA, 0, pd.NA],
    })
    cleaned = clean_covid_data(df)
    assert pd.isna(cleaned.loc[1, "Confirmed"])
    assert cleaned.loc[0, "Active"] == 4
    assert cleaned.loc[2, "Active"] == 3
    with_duplicates = pd.concat([cleaned, cleaned.iloc[[0]]], ignore_index=True)
    report = duplicate_report(with_duplicates)
    assert report["exact_duplicate_rows"] == 1
    assert len(remove_exact_duplicates(with_duplicates)) == len(cleaned)


def test_country_time_series_and_latest_data():
    df = pd.DataFrame({
        "Date": pd.to_datetime(["2021-01-01", "2021-01-01", "2021-01-02"]),
        "Country_Region": ["A", "A", "A"],
        "Province_State": ["P1", "P2", "P1"],
        "Confirmed": [10, 5, 20],
        "Deaths": [1, 0, 2],
        "Recovered": [2, 1, 10],
        "Active": [7, 4, 8],
    })
    daily = aggregate_country_daily(df)
    assert len(daily) == 2
    assert daily.loc[daily["Date"] == pd.Timestamp("2021-01-01"), "Confirmed"].iloc[0] == 15
    changes = add_daily_changes(daily)
    assert changes.loc[changes["Date"] == pd.Timestamp("2021-01-02"), "New_Confirmed"].iloc[0] == 5
    latest = get_latest_country_data(df)
    assert len(latest) == 1
    assert latest.iloc[0]["Date"] == pd.Timestamp("2021-01-02")
    assert latest.iloc[0]["Confirmed"] == 20
