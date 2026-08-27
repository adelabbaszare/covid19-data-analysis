# Data Quality and Time-Series Pipeline

## Date standardization

Each CSV receives a canonical `Date` column. The loader first tries to parse the
report date from the filename, supporting common historical formats such as:

- `MM-DD-YYYY.csv`
- `MM-DD-YY.csv`
- `YYYY-MM-DD.csv`

If no filename date can be extracted, the normalized `Last_Update` timestamp is
used as a fallback.

## Time-series aggregation

Daily reports can contain province, state, county, or other administrative rows.
Temporal country analysis therefore aggregates records by:

`Date + Country_Region`

before calculating daily changes. This prevents a single province from being
mistaken for the country total.

## Latest country data

The latest available date is calculated independently for each country. The result
contains country-level totals on that country's most recent report date.

## Missing values

The cleaning pipeline does not globally replace missing values with zero.

- Numeric values are converted safely with invalid values becoming missing.
- Negative epidemiological counts are treated as invalid.
- `Active` is derived only where Confirmed, Deaths, and Recovered are all
  available.
- Remaining missing values stay visible for analysis.

## Duplicates

Exact duplicate rows are removed. Key-based duplicates are reported using available
administrative keys but are not automatically deleted because they may represent
legitimate records requiring further domain validation.
