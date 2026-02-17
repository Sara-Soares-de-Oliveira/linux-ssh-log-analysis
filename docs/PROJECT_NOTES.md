# Project Reasoning and Methodology  

## Dataset
The dataset used in this project was obtained from Kaggle:

https://www.kaggle.com/datasets/ggsri123/linux-logs

It consists of Linux system logs, including authentication, kernel, network, and service-related events.

---

## Objective
The main goal of this project is to simulate a **Analysis of SSH authentication events**, focusing on:

- Identifying failed authentication attempts
- Extracting source hosts (rhost / IP or hostname)
- Identifying targeted users
- Preparing the data for further temporal and behavioral analysis

---

## Scope Definition

After manually inspecting the original log file, I defined a primary analytical scope:

- Include only SSH authentication-related events
- Exclude unrelated system noise (kernel, services, initialization logs)

This decision reduces complexity and reflects how a SOC analyst would narrow investigation scope during log triage.

---

## Filtering Strategy

### Inclusion Patterns
The following patterns were used to **include** relevant log entries:

- `sshd`
- `authentication`
- `Failed`
- `Accepted`
- `invalid user`
- `rhost`
- `user=`

These patterns capture SSH authentication activity, including failed logins, user enumeration attempts, and remote hosts.

---

### Exclusion Patterns
The following patterns were used to **exclude** unrelated system noise:

- `kernel`
- `systemd`
- `ftpd`
- `rc`
- `bluetooth`
- `init`

These services and subsystems are not relevant for SSH authentication analysis.

---

### Filtering Command
The following command was used to generate a cleaner dataset:

```bash
grep -E 'sshd|authentication|Failed|Accepted|invalid user|rhost|user=' Linux_2k.log \
| grep -v -e "kernel" -e "systemd" -e "bluetooth" -e "rc" -e "init" \
>> cleaned_logs.log 
```

As a result, the dataset was reduced from 1999 lines to 701 lines, making it significantly more manageable and focused

## Field Extraction Strategy

Tooling Decision

Initially, the plan was to use awk + regex. However, due to the variability of log formats and maintainability concerns, the approach was changed to:

Therefore, I decided to use:
	•	Python
	•	Regular Expressions (regex)

This choice allowed for:
	•	clearer logic
	•	easier debugging
	•	better extensibility as the project evolves

### Extraction Logic

For each log line:
	1.	Extract timestamp (syslog format)
	2.	Extract remote host (rhost)
	3.	Extract username (supports both user=<name> and user <name>)
	4.	Preserve original log line for traceability

Each event is stored as a dictionary and exported to a structured CSV file.

Some authentication lines do not contain an IP address. These were intentionally preserved to maintain completeness of authentication activity.

## Data Structuring

Each log entry is stored with the following fields:
	•	time
	•	rhost
	•	user
	•	raw_line (original log line)

All entries are then exported into a structured CSV file (log_data.csv) using Python’s csv.DictWriter.

### Temporal Enrichment

Because syslog timestamps do not include a year, an assumed year is added during preprocessing.

Derived time features include:
	•	complete_time (full datetime object)
	•	hour (for hourly distribution analysis)
	•	floor_minutes (minute-level aggregation for brute-force detection)

## Brute-Force Detection
Detection is based on behavioral aggregation.

Detection Rule

A source host generating ≥ 5 authentication attempts within a single minute
is flagged as suspicious.

Rationale
	•	Human users rarely generate multiple login attempts within such short intervals.
	•	Automated scripts and brute-force tools typically produce burst patterns.
	•	Minute-level bucketing allows identification of high-frequency attack behavior.

Limitations
	•	Low-and-slow attacks may not trigger this threshold.
	•	The dataset does not consistently differentiate between success and failure.
	•	Threshold is heuristic and not baseline-calibrated.


### Behavioral Indicators Considered
	•	Repeated authentication attempts from the same source host
	•	High concentration of attempts within short time windows
	•	Repeated targeting of common usernames (e.g., root, test)
	•	Temporal clustering suggesting automation


## Visual Analysis

Three primary visualizations were generated:
	1.	Top source hosts by authentication attempts
	2.	Authentication attempts per hour
	3.	Brute-force intensity (maximum attempts per minute per host)

These visuals support behavioral interpretation rather than raw counting.
	
## Current Status

At this stage, the project includes:
	•	Filtered dataset
	•	Structured CSV extraction
	•	Modular architecture (parser, utilities, analysis, visualization)
	•	Brute-force detection logic
	•	Exported detection results
	•	Generated visual reports

## Future Improvements
	•	Separate successful vs failed authentication explicitly
	•	Implement longer-window detection for low-and-slow attacks
	•	Integrate geolocation or IP reputation enrichment
	•	Translate detection logic into SIEM query format (e.g., Splunk/ELK)
	•	Develop automated reporting output

This project is intentionally iterative and will be refined as my knowledge grows.	
