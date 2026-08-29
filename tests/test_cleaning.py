import pandas as pd

from src.cleaning import clean_covid_data, duplicate_report, remove_exact_duplicates


def test_clean_covid_data_marks_negative_counts_missing_and_derives_active():
    frame = pd.DataFrame(
        {
            "Confirmed": [10, -1],
            "Deaths": [2, 1],
            "Recovered": [5, 1],
            "Active": [None, None],
        }
    )
    result = clean_covid_data(frame)
    assert result.loc[0, "Active"] == 3
    assert pd.isna(result.loc[1, "Confirmed"])


def test_duplicate_handling_removes_exact_duplicates_only():
    frame = pd.DataFrame({"Date": ["2021-01-01", "2021-01-01"], "Country_Region": ["A", "A"], "Confirmed": [1, 1]})
    report = duplicate_report(frame)
    assert report["exact_duplicate_rows"] == 1
    assert len(remove_exact_duplicates(frame)) == 1
