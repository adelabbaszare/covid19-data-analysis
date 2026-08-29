"""Project-wide paths and analysis configuration."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DEFAULT_NUMERIC_COLUMNS = (
    "Confirmed",
    "Deaths",
    "Recovered",
    "Active",
    "Incident_Rate",
    "Case_Fatality_Ratio",
    "Lat",
    "Long_",
)
