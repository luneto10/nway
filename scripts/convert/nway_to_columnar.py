#!/usr/bin/env python
"""
Convert nway combined set format to columnar format.

Input format (nway): Each line is a set with tab-separated intervals
  Set 0: 100 200	300 400	500 600
  Set 1: 150 250	350 450
  Set 2: 180 220	380 420

Output format (columnar): Each row is one interval across all sets
  start_0,end_0,start_1,end_1,start_2,end_2
  100,200,150,250,180,220
  300,400,350,450,380,420
  500,600,,,,

Note: If sets have different numbers of intervals, missing values are left empty.
"""
import sys
import csv
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-i",
    "--input",
    dest="input_file",
    help="Input combined set file (nway format: each line is a set)",
    default=None
)

parser.add_option(
    "-o",
    "--output",
    dest="output_file",
    help="Output CSV file (columnar format: each row is one interval)",
    default=None
)

parser.add_option(
    "-f",
    "--format",
    dest="output_format",
    help="Output format: 'csv' (default) or 'tsv'",
    default="csv"
)

(options, args) = parser.parse_args()

if not options.input_file:
    parser.error("Input file not given (-i)")

if not options.output_file:
    parser.error("Output file not given (-o)")

# Read all sets
sets = []
max_intervals = 0

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
            max_intervals = max(max_intervals, len(intervals))

if not sets:
    sys.stderr.write("Error: No valid sets found\n")
    sys.exit(1)

num_sets = len(sets)
sys.stderr.write(f"Converting {num_sets} sets with up to {max_intervals} intervals each\n")

# Determine delimiter
delimiter = ',' if options.output_format == 'csv' else '\t'

# Create output directory if it doesn't exist
import os
output_dir = os.path.dirname(options.output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# Write columnar format
with open(options.output_file, 'w', newline='') as f:
    writer = csv.writer(f, delimiter=delimiter)
    
    # Write header: start_0,end_0,start_1,end_1,...
    header = []
    for i in range(num_sets):
        header.extend([f'start_{i}', f'end_{i}'])
    writer.writerow(header)
    
    # Write data rows
    for row_idx in range(max_intervals):
        row = []
        for set_idx in range(num_sets):
            if row_idx < len(sets[set_idx]):
                start, end = sets[set_idx][row_idx]
                row.extend([start, end])
            else:
                # Empty cells for sets with fewer intervals
                row.extend(['', ''])
        writer.writerow(row)

sys.stderr.write(f"Converted to columnar format: {options.output_file}\n")
sys.stderr.write(f"Output: {max_intervals} rows × {num_sets * 2} columns\n")

