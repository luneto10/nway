#!/usr/bin/env python
"""
Convert columnar format to nway combined set format.

Input format (columnar): Each row is one interval across all sets
  start_0,end_0,start_1,end_1,start_2,end_2
  100,200,150,250,180,220
  300,400,350,450,380,420
  500,600,,,,

Output format (nway): Each line is a set with tab-separated intervals
  Set 0: 100 200	300 400	500 600
  Set 1: 150 250	350 450
  Set 2: 180 220	380 420

Note: Empty cells in input are skipped in output.
"""
import sys
import csv
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-i",
    "--input",
    dest="input_file",
    help="Input CSV/TSV file (columnar format: each row is one interval)",
    default=None
)

parser.add_option(
    "-o",
    "--output",
    dest="output_file",
    help="Output file (nway format: each line is a set)",
    default=None
)

parser.add_option(
    "-f",
    "--format",
    dest="input_format",
    help="Input format: 'csv' (default) or 'tsv'",
    default="csv"
)

(options, args) = parser.parse_args()

if not options.input_file:
    parser.error("Input file not given (-i)")

if not options.output_file:
    parser.error("Output file not given (-o)")

# Determine delimiter
delimiter = ',' if options.input_format == 'csv' else '\t'

# Read columnar data
sets = []
num_sets = 0

with open(options.input_file, 'r') as f:
    reader = csv.reader(f, delimiter=delimiter)
    
    # Read header to determine number of sets
    header = next(reader, None)
    if not header:
        sys.stderr.write("Error: Empty file or no header\n")
        sys.exit(1)
    
    # Count sets (each set has start and end columns)
    num_sets = len([col for col in header if col.startswith('start_')])
    sys.stderr.write(f"Detected {num_sets} sets from header\n")
    
    # Initialize sets
    sets = [[] for _ in range(num_sets)]
    
    # Read data rows
    for row in reader:
        if not row:
            continue
        
        # Process each set (start_i, end_i pairs)
        for set_idx in range(num_sets):
            start_col = set_idx * 2
            end_col = set_idx * 2 + 1
            
            if start_col < len(row) and end_col < len(row):
                start_str = row[start_col].strip()
                end_str = row[end_col].strip()
                
                if start_str and end_str:
                    try:
                        start = int(start_str)
                        end = int(end_str)
                        sets[set_idx].append((start, end))
                    except ValueError:
                        continue

if not sets:
    sys.stderr.write("Error: No valid intervals found\n")
    sys.exit(1)

# Create output directory if it doesn't exist
import os
output_dir = os.path.dirname(options.output_file)
if output_dir and not os.path.exists(output_dir):
    os.makedirs(output_dir, exist_ok=True)

# Write nway format
with open(options.output_file, 'w') as f:
    for set_idx, intervals in enumerate(sets):
        if intervals:
            # Format: "start end\tstart end\t..."
            line = '\t'.join([f"{start} {end}" for start, end in intervals])
            f.write(line + '\n')
        else:
            # Empty set - write empty line
            f.write('\n')

sys.stderr.write(f"Converted to nway format: {options.output_file}\n")
sys.stderr.write(f"Output: {len(sets)} sets\n")
for i, intervals in enumerate(sets):
    sys.stderr.write(f"  Set {i}: {len(intervals)} intervals\n")

