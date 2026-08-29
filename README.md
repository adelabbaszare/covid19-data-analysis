# 🦠 COVID-19 Pandemic Data Analysis

![COVID-19 Pandemic Data Analysis](./COVID-19-Analysis.jpg)

A reproducible Python project for loading, standardizing, cleaning, and analyzing historical COVID-19 daily reports.

## Project Structure

```text
.
├── data/
│   ├── raw/              # Local raw CSV reports (ignored by Git)
│   ├── interim/          # Intermediate datasets (ignored by Git)
│   ├── processed/        # Derived datasets (ignored by Git)
│   └── README.md         # Dataset and reproducibility notes
├── docs/
│   ├── schema_analysis.md
│   └── data_quality_pipeline.md
├── scripts/
│   └── download_data.py  # Reproducible raw-report downloader
├── src/
│   ├── __init__.py
│   ├── config.py         # Project paths and shared configuration
│   ├── schema.py         # Schema normalization and date parsing
│   ├── cleaning.py       # Missing values and duplicate handling
│   ├── analysis.py       # Country/time-series analysis
│   └── data_loader.py    # Small loading facade for notebooks/backward compatibility
├── tests/
│   └── test_data_loader.py
├── COVID-19_Analysis_Notebook.ipynb
├── requirements.txt
└── .gitignore
```

## Architecture

The project separates reusable logic from presentation:

```text
Raw CSV files
    ↓
 data_loader.py
    ↓
 schema.py
    ↓
 cleaning.py
    ↓
 analysis.py
    ↓
 Jupyter Notebook / Results
```

The notebook remains focused on analysis and visualization, while reusable data-processing logic lives under `src/`.

## Installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Dataset

Raw COVID-19 daily reports are intentionally **not committed** to this repository. The project is based on the archived Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) COVID-19 repository. JHU documents the daily-report naming convention as `MM-DD-YYYY.csv` and notes that global reporting ceased on March 10, 2023. citeturn800665search0turn800665search1

Download selected reports into `data/raw/`:

```bash
python scripts/download_data.py 01-01-2021 01-02-2021 01-03-2021
```

The exact date range used for a final analysis should be recorded in project documentation or, preferably, a future dataset manifest with source revision and checksums.

See [`data/README.md`](./data/README.md) for the data policy.

## Load Data

```python
from src.data_loader import load_covid_data

df = load_covid_data("data/raw")
```

## Schema Normalization

Historical reports used different names for equivalent fields. The project normalizes aliases such as:

- `Country/Region` → `Country_Region`
- `Province/State` → `Province_State`
- `Last Update` → `Last_Update`
- `Latitude` → `Lat`
- `Longitude` → `Long_`

See [`docs/schema_analysis.md`](./docs/schema_analysis.md).

## Tests

```bash
pytest
```
