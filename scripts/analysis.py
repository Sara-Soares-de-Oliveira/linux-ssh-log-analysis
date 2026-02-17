"""
SOC Project - Brute-force Detection (SSH Logs)

This script loads a structured CSV dataset generated from Linux logs, filters
events that contain a source host (rhost), enriches the dataset with time
features (hour and minute bucket), and detects potential brute-force behavior
based on a simple threshold rule.

Output:
- results/bruteforce_windows.csv
  Contains (rhost, floor_minutes, count) for suspicious time windows.
"""

from __future__ import annotations

from utils import add_time_features, filter_attack_events, load_data


THRESHOLD = 5
"""
Attempts in the same minute to flag a source host as suspicious.

Rationale:
- A human is unlikely to generate multiple authentication attempts within a
  single minute repeatedly.
- Automated scripts commonly generate high-frequency bursts in short windows.

Note:
- This threshold is a heuristic for portfolio/demo purposes and may require
  tuning for real environments.
"""


def detect_bruteforce_windows(df, threshold: int = THRESHOLD):
    """
    Detect brute-force-like behavior using minute-based aggregation.

    The detection logic groups events by:
    - rhost: source host (IP/hostname)
    - floor_minutes: timestamp normalized to 1-minute windows

    For each (rhost, minute) pair, it counts how many events occurred.
    Any group with count >= threshold is flagged as suspicious.

    Args:
        df: Prepared DataFrame that includes 'rhost' and 'floor_minutes'.
        threshold: Minimum number of events in the same minute to flag.

    Returns:
        A DataFrame with columns: ['rhost', 'floor_minutes', 'count'] containing
        only suspicious windows.
    """
    grouped = (
        df.groupby(["rhost", "floor_minutes"])
        .size()
        .reset_index(name="count")
    )
    return grouped[grouped["count"] >= threshold]


def main() -> None:
    """
    Run the brute-force detection pipeline end-to-end.

    Steps:
    1) Load structured CSV data (results/log_data.csv)
    2) Filter out events without a source host (rhost)
    3) Add time features (complete_time, hour, floor_minutes)
    4) Detect suspicious brute-force windows using a threshold rule
    5) Export detection results to results/bruteforce_windows.csv
    """
    df = load_data("./results/log_data.csv")
    df = filter_attack_events(df)
    df = add_time_features(df, "2026")

    bruteforce_events = detect_bruteforce_windows(df, threshold=THRESHOLD)

    bruteforce_events.to_csv("./results/bruteforce_windows.csv", index=False)

    print("Brute-force detection completed.")
    print(f"Total suspicious windows detected: {len(bruteforce_events)}")


if __name__ == "__main__":
    main()