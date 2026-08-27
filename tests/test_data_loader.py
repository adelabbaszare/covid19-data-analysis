import pandas as pd

from src.data_loader import standardize_schema


def test_standardize_schema_merges_historical_column_names():
    df = pd.DataFrame({"Country_Region": ["A", None], "Country/Region": [None, "B"], "Province/State": ["P1", "P2"], "Latitude": [10.0, 20.0], "Last Update": ["2021-01-01", "2021-01-02"]})
    result = standardize_schema(df)
    assert "Country/Region" not in result.columns
    assert result["Country_Region"].tolist() == ["A", "B"]
    assert "Province_State" in result.columns
    assert "Lat" in result.columns
    assert pd.api.types.is_datetime64_any_dtype(result["Last_Update"])
