import pandas as pd

from src.schema import extract_date_from_filename, standardize_schema


def test_extract_date_from_filename():
    assert extract_date_from_filename("01-02-2021.csv") == pd.Timestamp("2021-01-02")
    assert extract_date_from_filename("2021-01-02.csv") == pd.Timestamp("2021-01-02")


def test_standardize_schema_coalesces_aliases():
    frame = pd.DataFrame(
        {
            "Country_Region": ["A", None],
            "Country/Region": [None, "B"],
            "Province/State": ["P1", "P2"],
            "Last Update": ["2021-01-01 00:00:00", "2021-01-02 00:00:00"],
        }
    )
    result = standardize_schema(frame)
    assert result["Country_Region"].tolist() == ["A", "B"]
    assert "Country/Region" not in result.columns
    assert "Province_State" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["Last_Update"])
