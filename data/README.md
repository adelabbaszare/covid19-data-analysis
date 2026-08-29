# Dataset

Raw CSV reports are intentionally not committed to the repository. The analysis is based on historical daily reports from the Johns Hopkins University Center for Systems Science and Engineering (JHU CSSE) COVID-19 repository.

JHU documents the daily-report naming convention as `MM-DD-YYYY.csv` and states that the repository was archived after global reporting ceased on March 10, 2023. The archived reports remain available for reproducibility.

## Recommended workflow

1. Keep `data/raw/` local and untracked.
2. Download the exact report dates required for an analysis run with `scripts/download_data.py`.
3. Record the selected date range and source revision in the project documentation or a future manifest file.
4. Keep cleaned/derived datasets under `data/interim/` or `data/processed/`, also untracked.

Example:

```bash
python scripts/download_data.py 01-01-2021 01-02-2021 01-03-2021
```

For a complete historical snapshot, prefer an external archive/repository release or Git LFS rather than ordinary Git commits, because the full daily-report collection is large.
