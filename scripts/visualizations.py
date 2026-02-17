"""
SOC Project - Visualizations

This script generates visual representations of SSH authentication activity
based on the structured dataset produced by the analyzer.

Generated figures:
1) Top source hosts (horizontal bar chart)
2) Authentication attempts per hour (line chart)
3) Brute-force intensity per host (bar chart)

Output:
- results/figures/top_hosts.png
- results/figures/attempts_per_hour.png
- results/figures/bruteforce_intensity.png
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from utils import add_time_features, filter_attack_events, load_data


OUTPUT_DIR = Path("./results/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_top_hosts(df: pd.DataFrame, top_n: int = 10) -> None:
    """
    Plot top N source hosts by authentication attempts.
    """
    top_hosts = df["rhost"].value_counts().head(top_n)

    plt.figure(figsize=(12, 6))
    top_hosts.sort_values().plot(kind="barh")
    plt.title("Top Source Hosts by Authentication Attempts")
    plt.xlabel("Number of Attempts")
    plt.ylabel("Source Host")


    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "top_hosts.png")
    plt.close()


def plot_attempts_per_hour(df: pd.DataFrame) -> None:
    """
    Plot authentication attempts distributed by hour of day.
    """
    hourly_counts = df["hour"].value_counts().sort_index()

    plt.figure(figsize=(12, 6)) 
    hourly_counts.plot(kind="line")
    plt.title("Authentication Attempts per Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Attempts")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "attempts_per_hour.png")
    plt.close()


def plot_bruteforce_intensity(df: pd.DataFrame, threshold: int = 5) -> None:
    """
    Plot brute-force intensity per host (max attempts in a single minute).
    """
    grouped = (
        df.groupby(["rhost", "floor_minutes"])
        .size()
        .reset_index(name="count")
    )

    suspicious = grouped[grouped["count"] >= threshold]

    if suspicious.empty:
        print("No brute-force windows detected.")
        return

    max_per_host = (
        suspicious.groupby("rhost")["count"]
        .max()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))
    max_per_host.head(10).sort_values().plot(kind="barh")
    plt.title("Brute-force Intensity (Max Attempts per Minute)")
    plt.xlabel("Max Attempts in One Minute")
    plt.ylabel("Source Host")
    

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "bruteforce_intensity.png")
    plt.close()


def main() -> None:
    """
    Run visualization pipeline.
    """
    df = load_data("./results/log_data.csv")
    df = filter_attack_events(df)
    df = add_time_features(df, "2026")

    plot_top_hosts(df)
    plot_attempts_per_hour(df)
    plot_bruteforce_intensity(df)

    print("Visualizations generated successfully.")
    print(f"Saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()