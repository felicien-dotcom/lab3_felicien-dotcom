#!/bin/bash
# feed-analyzer.sh - Top 5 most active users in twitter_dataset.csv
# Usage: ./feed-analyzer.sh twitter_dataset.csv

FILE="$1"

if [ -z "$FILE" ]; then
    echo "Error: no input file given."
    echo "Usage: ./feed-analyzer.sh twitter_dataset.csv"
    exit 1
fi
if [ ! -f "$FILE" ]; then
    echo "Error: file '$FILE' not found."
    exit 1
fi

COL=$(head -n 1 "$FILE" | tr -d '\r' | tr ',' '\n' | grep -n -x -i 'Username' | cut -d: -f1)
if [ -z "$COL" ]; then
    echo "Error: no 'Username' column found in the header of '$FILE'."
    exit 1
fi


echo "Top 5 Most Active Users"
echo "-----------------------"
echo "Posts  Username"
awk -F',' -v col="$COL" '
    NR == 1 { next }                      # skip the header row
    inq == 0 { gsub(/\r/, ""); if ($col != "") print $col }   # start of a new tweet
    { n = gsub(/"/, "\""); if (n % 2 == 1) inq = !inq }       # track open quotes
' "$FILE" \
  | sort \
  | uniq -c \
  | sort -nr \
  | head -n 5
