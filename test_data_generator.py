#!/usr/bin/env python3
"""
Generate a test data file with 10,000 rows:
- Column 1: intstdwv (float)
- Column 2: sample name ("NIST612 - <row_index>")
- Columns 3..22: 20 random float columns
Output: test_data.csv
"""

import csv
import random

OUTFILE = "test_data.csv"
ROWS = 100_000_000
RANDOM_COLS = 20
FLOAT_MIN = 0.0
FLOAT_MAX = 100.0
DELIMITER = ","  # change to "\t" for TSV or " " for space-separated

def random_float():
    return round(random.uniform(FLOAT_MIN, FLOAT_MAX), 6)

def generate_row(idx):
    intstdwv = random_float()
    sample_name = f"NIST612 - {idx}"
    random_cols = [random_float() for _ in range(RANDOM_COLS)]
    return [intstdwv, sample_name] + random_cols

def main():
    with open(OUTFILE, "w", newline="") as f:
        writer = csv.writer(f, delimiter=DELIMITER)
        # header (optional)
        header = ["intstdwv", "sample_name"] + [f"col_{i+1}" for i in range(RANDOM_COLS)]
        writer.writerow(header)
        for i in range(1, ROWS + 1):
            writer.writerow(generate_row(i))

if __name__ == "__main__":
    main()
