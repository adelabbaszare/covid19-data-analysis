# 🦠 COVID-19 Pandemic Data Analysis

![COVID-19 Pandemic Data Analysis](./COVID-19-Analysis.jpg)

A reproducible Python project for loading, standardizing, cleaning, analyzing, and visualizing historical COVID-19 daily reports.

[فارسی](./README_fa.md)

## ✨ Highlights

- Reusable data-loading and schema-normalization pipeline.
- Historical report-date extraction and country-level time-series aggregation.
- Conservative handling of missing and invalid values.
- Exact-duplicate removal with administrative-key duplicate reporting.
- Reusable visualization helpers for global, country, and top-country analysis.
- Automated tests, linting, import-order checks, and formatting checks with GitHub Actions.
- Raw source data kept outside Git history for a smaller and reproducible repository.

## 🧱 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── raw/                 # Downloaded source CSV files (Git-ignored)
│   ├── interim/             # Intermediate datasets (Git-ignored)
│   ├── processed/           # Derived datasets (Git-ignored)
│   └── README.md
├── docs/
│   ├── schema_analysis.md
│   └── data_quality_pipeline.md
├── scripts/
│   └── download_data.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── schema.py
│   ├── cleaning.py
│   ├── analysis.py
│   ├── visualization.py
│   └── data_loader.py
├── tests/
│   └── test_data_loader.py
├── COVID-19_Analysis_Notebook.ipynb
├── pyproject.toml
├── requirements.txt
├── README.md
└── README_fa.md
```

## 🔄 Architecture

```text
Raw CSV Reports
      ↓
 data_loader.py
      ↓
   schema.py
      ↓
  cleaning.py
      ↓
  analysis.py
      ↓
visualization.py
      ↓
 Jupyter Notebook
```

The notebook is intentionally focused on exploration, interpretation, and presentation. Reusable logic lives in `src/` and is independently testable.

## 🚀 Installation

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 📦 Dataset

Raw COVID-19 reports are not committed to Git. They are downloaded into `data/raw/` when needed. The project currently targets the archived Johns Hopkins University CSSE COVID-19 daily reports.

Example:

```bash
python scripts/download_data.py 01-01-2021 01-02-2021 01-03-2021
```

For a reproducible run, record the exact report dates and upstream revision used for the analysis. See [`data/README.md`](./data/README.md).

## ▶️ Run the Notebook

Open `COVID-19_Analysis_Notebook.ipynb` in Jupyter Lab, Jupyter Notebook, or Google Colab after placing the required CSV reports under `data/raw/`.

## 🧪 Tests

```bash
pytest -q
```

## 🧹 Code Quality

The project uses Black, isort, and Ruff. CI runs a single quality job on Python 3.11 and checks formatting, import ordering, linting, and tests.

```bash
black src tests
isort src tests
ruff check src tests
pytest -q
```

## 📊 Visualization

Reusable plotting functions are available in `src/visualization.py` for:

- Global cumulative trends.
- Country-level trends.
- Top countries by a selected metric.

The notebook imports these helpers instead of embedding plotting logic repeatedly.

## 📚 Documentation

- [`docs/schema_analysis.md`](./docs/schema_analysis.md) — historical schema differences.
- [`docs/data_quality_pipeline.md`](./docs/data_quality_pipeline.md) — date, cleaning, aggregation, and duplicate policies.

## 📄 License

Add the appropriate license before redistributing the dataset, code, or derived materials.
