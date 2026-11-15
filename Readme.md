# Lab 3 – Data Detective & Feed Analyzer

Analyzes `twitter_dataset.csv` with Python and Bash.

## Files
- `data-detective.py` – Python app (Quests 1–4)
- `feed-analyzer.sh` – Bash script: Top 5 most active users
- `twitter_dataset.csv` – the dataset

## How to run
```bash
python3 data-detective.py
chmod +x feed-analyzer.sh
./feed-analyzer.sh twitter_dataset.csv
```

## What each part does
| Quest | Description |
|-------|-------------|
| 1 – Data Auditor | Removes tweets with no Text; replaces blank/invalid Likes and Retweets with `0`; prints how many rows were removed/fixed. |
| 2 – Viral Post | Loops through tweets to find the highest Likes; prints Username, Likes and Text. |
| 3 – Algorithm Builder | Own **Selection Sort** (no `.sort()`), highest Likes first; slices the top 10. |
| 4 – Content Filter | Asks for a search word (case-insensitive), builds a new list of matches, prints `len()` then the tweets. |
| Shell script | `awk` (reads the Username, handling tweets that span several lines) → `sort` → `uniq -c` → `sort -nr` → `head -n 5` to show the 5 most active users. |

## Note on libraries
No external libraries are used. The only import is Python's built-in `csv` module, used solely to read
the file correctly because tweet text can contain commas inside quotes. All cleaning, searching and
sorting logic is written by hand.

## Error handling
Missing file, empty file, missing columns, empty search input and invalid menu choices all show a clear message.
