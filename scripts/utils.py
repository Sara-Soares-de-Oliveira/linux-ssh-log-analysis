"""
SOC Project - Utilities

This module contains shared helper functions used across the project scripts.
It centralizes common tasks such as:

- loading the structured CSV dataset
- filtering events that can be attributed to an external source (rhost)
- enriching data with time-based features for aggregation and detection

These functions are intentionally side-effect free (no printing, no plotting)
to keep them reusable by both analysis and visualization scripts.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd


def load_data(path: str) -> pd.DataFrame:
    """
    Load a CSV file and return it as a pandas DataFrame.

    Args:
        path: Path to the CSV file.

    Returns:
        A pandas DataFrame containing the loaded data.
    """
    return pd.read_csv(path)


def filter_attack_events(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filter the dataset to keep only events with an identifiable source host.

    Events without 'rhost' cannot be attributed to an external source and are
    excluded for attack-focused analysis (e.g., brute-force detection).

    Args:
        df: Input DataFrame.

    Returns:
        A new DataFrame containing only rows where 'rhost' is present.
    """
    filtered = df.dropna(subset=["rhost"]).copy()

    # Normalize rhost values (helps grouping and counting).
    filtered["rhost"] = filtered["rhost"].astype(str).str.strip()

    # Remove empty strings if they exist (e.g., " ").
    filtered = filtered[filtered["rhost"] != ""]

    return filtered


def add_time_features(df: pd.DataFrame, year: str) -> pd.DataFrame:
    """
    Add derived time columns for temporal analysis and brute-force detection.

    The source log timestamp (e.g., "Jun 14 15:16:01") does not include a year.
    This function prepends a chosen year (for consistency) and converts the
    timestamp to datetime, then creates additional time-based fields.

    Added columns:
        - complete_time: datetime built from assumed year + original timestamp
        - hour: integer hour of day (0–23), useful for peak-hour analysis
        - floor_minutes: datetime floored to minute, used for brute-force windows

    Args:
        df: Input DataFrame containing a 'time' column.
        year: Year to assume for the timestamps (e.g., "2026").

    Returns:
        A new DataFrame with added time-derived columns.

    Raises:
        KeyError: If the 'time' column is missing.
        ValueError: If timestamps do not match the expected syslog format.
    """
    df = df.copy()

    full_time = year + " " + df["time"].astype(str).str.strip()
    df["complete_time"] = pd.to_datetime(full_time, format="%Y %b %d %H:%M:%S")

    df["hour"] = df["complete_time"].dt.hour
    df["floor_minutes"] = df["complete_time"].dt.floor("min")

    return df