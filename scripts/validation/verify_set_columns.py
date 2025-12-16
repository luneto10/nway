#!/usr/bin/env python
"""
Verify if intervals at the same column position across sets are sorted.

Each line in the input file is a set.
Each set has intervals separated by tabs: "start end\tstart end\t..."

This script checks if intervals at the same column position (same interval_index)
across different sets are sorted by their start position.
"""
import sys
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-f",
    "--file",
    dest="input_file",
    help="Input combined set file",
    default=None
)

(options, args) = parser.parse_args()

if not options.input_file:
    parser.error("Input file not given")

# Read all sets
sets = []
with open(options.input_file, 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        intervals = []
        for interval_str in line.split('\t'):
            parts = interval_str.strip().split()
            if len(parts) == 2:
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                    intervals.append((start, end))
                except ValueError:
                    continue
        if intervals:
            sets.append(intervals)

if not sets:
    sys.stderr.write("Error: No valid sets found\n")
    sys.exit(1)

# Find maximum number of intervals (columns)
max_cols = max(len(s) for s in sets)

sys.stderr.write(f"Found {len(sets)} sets with up to {max_cols} intervals each\n")

# Check each column
all_sorted = True
for col_idx in range(max_cols):
    column_values = []
    for set_idx, intervals in enumerate(sets):
        if col_idx < len(intervals):
            start, end = intervals[col_idx]
            column_values.append((set_idx, start, end))
    
    if len(column_values) < 2:
        continue
    
    # Check if sorted by start
    is_sorted = True
    for i in range(len(column_values) - 1):
        if column_values[i][1] > column_values[i+1][1]:
            is_sorted = False
            break
    
    if not is_sorted:
        all_sorted = False
        sys.stderr.write(f"Column {col_idx} is NOT sorted:\n")
        for set_idx, start, end in column_values:
            sys.stderr.write(f"  Set {set_idx}: {start} {end}\n")
    else:
        sys.stderr.write(f"Column {col_idx} is sorted ({len(column_values)} intervals)\n")

if all_sorted:
    sys.stderr.write("\n✓ All columns are sorted!\n")
    sys.exit(0)
else:
    sys.stderr.write("\n✗ Some columns are not sorted. Consider using combine_sets_sorted.py with -s flag.\n")
    sys.exit(1)

