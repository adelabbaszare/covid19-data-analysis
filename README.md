# 🦠 Comprehensive COVID-19 Pandemic Data Analysis

A reproducible Python project for loading, standardizing, cleaning, and analyzing historical COVID-19 datasets.

## Project Structure

```text
.
├── data/
│   ├── raw/          # Source CSV files (not committed)
│   ├── interim/      # Intermediate outputs
│   └── processed/    # Cleaned datasets
├── docs/
│   └── schema_analysis.md
├── notebooks/
├── src/
│   ├── __init__.py
│   └── data_loader.py
├── tests/
│   └── test_data_loader.py
├── COVID-19_Analysis_Notebook.ipynb
├── requirements.txt
└── .gitignore
```

## Key Improvements

- Centralized CSV discovery and loading.
- Removed dependency on hardcoded Windows paths.
- Added schema inspection utilities.
- Standardized historical column-name variations before concatenation.
- Added `Source_File` for data traceability.
- Added a minimal automated test for schema normalization.

## Installation

```bash
pip install -r requirements.txt
```

## Loading Data

Place CSV files inside `data/raw/` and use:

```python
from src.data_loader import load_covid_data

df = load_covid_data("data/raw")
```

For schema inspection:

```python
from src.data_loader import discover_csv_files, inspect_schema

files = discover_csv_files("data/raw")
report = inspect_schema(files)
print(report)
```

## Schema Normalization

Historical data sources may use different names for the same concept, such as:

- `Country/Region` → `Country_Region`
- `Province/State` → `Province_State`
- `Last Update` → `Last_Update`
- `Latitude` → `Lat`
- `Longitude` → `Long_`

See `docs/schema_analysis.md` for details.

## Data Source

The analysis uses historical public COVID-19 daily reports. The exact source files and their acquisition process should be documented alongside the raw dataset used for a reproducible run.

## Testing

```bash
pytest
```
