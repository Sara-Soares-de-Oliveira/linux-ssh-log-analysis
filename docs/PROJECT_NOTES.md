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

## Initial Log Analysis and Scope Definition
After manually inspecting the original log file, I defined a **primary scope** focused exclusively on:

- SSH-related events
- Authentication attempts (successful or failed)

All other system events were considered noise for the purpose of this project.

This step was essential to reduce complexity and work with a dataset that reflects a realistic investigation scenario.

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

### Field Extraction Strategy

Tooling Decision

Initially, the plan was to use awk + regex, but this approach proved too complex and hard to maintain for multiple log formats.

Therefore, I decided to use:
	•	Python
	•	Regular Expressions (regex)

This choice allowed for:
	•	clearer logic
	•	easier debugging
	•	better extensibility as the project evolves

### Extraction Logic

The extraction process follows this logic:
	1.	Read the filtered log file line by line
	2.	Attempt to extract:
	•	timestamp
	•	remote host (rhost)
	•	username (user=… or user <name>)
	3.	Store each log entry as a dictionary
	4.	Append each dictionary to a list (one event per log line)

Some authentication-related lines do not contain an IP address. These lines were intentionally preserved to maintain data completeness.

The extraction process was implemented using re.search() and capture groups.

## Data Structuring

Each log entry is stored with the following fields:
	•	time
	•	rhost
	•	user
	•	raw_line (original log line)

All entries are then exported into a structured CSV file (log_data.csv) using Python’s csv.DictWriter.

## Scripts Overview
•	analyzer.py
    Responsible for:
	•	reading the filtered log file
	•	extracting relevant fields
	•	building dictionaries
	•	exporting the structured CSV

•	analysis.py
    Reserved for data analysis tasks, such as:
	•	top attacking hosts
	•	most targeted users
	•	temporal analysis (in progress)
	
## Current Status

At this stage, the project includes:
	•	a filtered and scoped dataset
	•	a structured CSV ready for analysis
	•	initial exploratory analysis (basic prints)

Further analysis (temporal patterns, brute-force detection, and visualization) will be added as the project evolves.

## Future Improvements
	•	Correlate authentication failures with timestamps to detect brute-force behavior
	•	Add hourly and daily aggregation
	•	Visualize attack patterns
	•	Improve parsing logic as regex skills evolve

This project is intentionally iterative and will be refined as my knowledge grows.	
