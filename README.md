# Linux SSH Log Analysis 

This project simulates a **analysis of Linux SSH authentication logs**.

The focus is on:
- filtering noisy system logs
- extracting relevant SSH authentication events
- structuring the data for analysis
- preparing the dataset for detection of suspicious behavior (e.g. brute-force)

---

## Dataset
Source:  
https://www.kaggle.com/datasets/ggsri123/linux-logs

---

## How It Works
1. Filter original Linux logs to keep only SSH/authentication-related events
2. Extract key fields (timestamp, rhost, user, raw log line)
3. Export structured data to CSV
4. Perform analysis using Python (in progress)

---

## How to Run

### Requirements
- Python 3.x

Install dependencies (optional but recommended for analysis):
```bash
pip install -r requirements.txt
```

---

### Documentation
Detailed reasoning and methodology can be found in:

- `docs/PROJECT_NOTES.md` 

---

### Notes
•	This project is intentionally iterative.
•	Parsing logic and analysis will evolve as skills improve.

---

## Author
Sara Oliveira
- [LinkedIn](https://www.linkedin.com/in/sara-oliveira-055a35278/)

