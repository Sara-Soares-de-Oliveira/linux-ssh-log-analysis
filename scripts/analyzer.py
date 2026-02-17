"""
SOC Project - Log Parser (SSH/Auth Events)

This script reads a filtered Linux log file (cleaned_logs.log), extracts
key fields using regular expressions, and exports a structured CSV dataset.

Extracted fields:
- time: syslog-style timestamp (month day hh:mm:ss)
- rhost: source host/IP (when present)
- user: username (supports both 'user=<name>' and 'user <name>' patterns)
- raw_line: original log line (trimmed)

Output:
- results/log_data.csv
"""

from __future__ import annotations

import csv
import re
from pathlib import Path


DATE_PATTERN = re.compile(r"\b[A-Z][a-z]{2}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}\b")
RHOST_PATTERN = re.compile(r"(?<=rhost=)\S+")
USER_PATTERN = re.compile(r"(?<=user[ ]|user=)\S+")

FIELDNAMES = ["time", "rhost", "user", "raw_line"]


def parse_log_line(line: str) -> dict[str, str | None]:
    """
    Parse a single log line and extract fields.

    Args:
        line: Raw log line.

    Returns:
        A dictionary with keys: time, rhost, user, raw_line.
        Missing values are returned as None.
    """
    date_match = DATE_PATTERN.search(line)
    rhost_match = RHOST_PATTERN.search(line)
    user_match = USER_PATTERN.search(line)

    timestamp = date_match.group() if date_match else None
    rhost = rhost_match.group() if rhost_match else None
    user = user_match.group() if user_match else None

    return {
        "time": timestamp,
        "rhost": rhost,
        "user": user,
        "raw_line": line.rstrip(),
    }


def parse_log_file(input_path: Path) -> list[dict[str, str | None]]:
    """
    Parse an entire log file into structured records.

    Args:
        input_path: Path to the cleaned log file.

    Returns:
        A list of dictionaries (one per log line).
    """
    records: list[dict[str, str | None]] = []

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        for line in f:
            records.append(parse_log_line(line))

    return records


def write_csv(records: list[dict[str, str | None]], output_path: Path) -> None:
    """
    Write parsed log records to a CSV file.

    Args:
        records: List of parsed log dictionaries.
        output_path: Destination CSV path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=FIELDNAMES,
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        writer.writerows(records)


def main() -> None:
    """
    Run the log parsing pipeline end-to-end.

    Steps:
    1) Read cleaned_logs.log
    2) Extract fields using regex
    3) Export results/log_data.csv
    """
    input_path = Path("./data/cleaned_logs.log")
    output_path = Path("./results/log_data.csv")

    records = parse_log_file(input_path)
    write_csv(records, output_path)

    print("Log parsing completed.")
    print(f"Input: {input_path}")
    print(f"Output: {output_path}")
    print(f"Total records: {len(records)}")


if __name__ == "__main__":
    main()