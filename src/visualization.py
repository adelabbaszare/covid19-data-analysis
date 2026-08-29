"""Reusable visualization helpers for COVID-19 analysis."""

import matplotlib.pyplot as plt


def plot_global_trends(global_daily, metrics=None, figsize=(12, 6)):
    """Plot cumulative global COVID-19 trends."""
    metrics = metrics or ["Confirmed", "Deaths", "Recovered", "Active"]
    metrics = [column for column in metrics if column in global_daily.columns]
    if not metrics:
        raise ValueError("No requested metrics are available for plotting.")

    ax = global_daily.set_index("Date")[metrics].plot(figsize=figsize)
    ax.set_title("Global COVID-19 Cumulative Trends")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    return ax


def plot_country_trends(country_daily, country, metrics=None, figsize=(12, 6)):
    """Plot cumulative and/or daily metrics for one country."""
    metrics = metrics or ["Confirmed", "Deaths", "Recovered", "Active"]
    metrics = [column for column in metrics if column in country_daily.columns]
    data = country_daily[country_daily["Country_Region"].eq(country)]
    if data.empty:
        raise ValueError(f"Country not found: {country}")
    if not metrics:
        raise ValueError("No requested metrics are available for plotting.")

    ax = data.set_index("Date")[metrics].plot(figsize=figsize)
    ax.set_title(f"COVID-19 Trends — {country}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")
    ax.grid(True, alpha=0.25)
    plt.tight_layout()
    return ax


def plot_top_countries(
    latest_country_data, metric="Confirmed", top_n=10, figsize=(10, 6)
):
    """Plot the top countries by a latest-available cumulative metric."""
    required = {"Country_Region", metric}
    missing = required.difference(latest_country_data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data = latest_country_data.nlargest(top_n, metric).sort_values(metric)
    ax = data.plot.barh(x="Country_Region", y=metric, legend=False, figsize=figsize)
    ax.set_title(f"Top {len(data)} Countries by {metric}")
    ax.set_xlabel("Cases")
    ax.set_ylabel("Country")
    ax.grid(True, axis="x", alpha=0.25)
    plt.tight_layout()
    return ax
