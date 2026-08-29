"""Download selected JHU CSSE daily COVID-19 reports into data/raw/.

The upstream JHU repository is an archived public data source. This script keeps
large raw data files out of this repository while making the dataset reproducible.
"""
from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

BASE_URL = (
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/"
    "master/csse_covid_19_data/csse_covid_19_daily_reports/"
)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "raw"


def download_report(date: str, output_dir: Path) -> Path:
    filename = f"{date}.csv"
    destination = output_dir / filename
    output_dir.mkdir(parents=True, exist_ok=True)

    if destination.exists():
        print(f"Already exists: {destination}")
        return destination

    url = BASE_URL + filename
    try:
        with urlopen(url, timeout=30) as response:
            destination.write_bytes(response.read())
    except (HTTPError, URLError) as exc:
        raise RuntimeError(f"Could not download {url}: {exc}") from exc

    print(f"Downloaded: {destination}")
    return destination


def main() -> None:
    parser = ArgumentParser(description="Download JHU CSSE COVID-19 daily reports.")
    parser.add_argument("dates", nargs="+", help="Dates such as 01-01-2021")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    args = parser.parse_args()

    for date in args.dates:
        download_report(date, args.output_dir)


if __name__ == "__main__":
    main()
