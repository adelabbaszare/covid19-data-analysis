import pandas as pd

from src.analysis import (
    add_daily_changes,
    aggregate_country_daily,
    get_latest_country_data,
)


def sample_data():
    return pd.DataFrame(
        {
            "Date": pd.to_datetime(["2021-01-01", "2021-01-01", "2021-01-02"]),
            "Country_Region": ["A", "A", "A"],
            "Province_State": ["P1", "P2", "P1"],
            "Confirmed": [10, 5, 20],
            "Deaths": [1, 0, 2],
            "Recovered": [4, 2, 10],
            "Active": [5, 3, 8],
        }
    )


def test_aggregate_country_daily_sums_regions():
    result = aggregate_country_daily(sample_data())
    day1 = result[result["Date"].eq(pd.Timestamp("2021-01-01"))].iloc[0]
    assert day1["Confirmed"] == 15
    assert day1["Deaths"] == 1


def test_daily_changes_are_grouped_by_country():
    result = add_daily_changes(aggregate_country_daily(sample_data()))
    day2 = result[result["Date"].eq(pd.Timestamp("2021-01-02"))].iloc[0]
    assert day2["New_Confirmed"] == 5


def test_latest_country_data_uses_country_specific_latest_date():
    frame = sample_data()
    frame.loc[len(frame)] = [pd.Timestamp("2021-01-03"), "B", "P1", 7, 1, 3, 3]
    result = get_latest_country_data(frame)
    assert set(result["Country_Region"]) == {"A", "B"}
    assert result.loc[result["Country_Region"].eq("A"), "Date"].iloc[0] == pd.Timestamp(
        "2021-01-02"
    )
