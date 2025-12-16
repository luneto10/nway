#!/usr/bin/env python
"""
Combine multiple .set files into a single file for nway input, ensuring column-wise sorting.

Each .set file should contain a single line with tab-separated intervals.
The output file will have one line per input file, where each line represents one set.

When combining sets, intervals at the same column position (same interval_index)
across different sets are sorted by their start position. Start/end pairs move together.

Example:
  Set 0: 3 13    2 7     2 10    8 16
  Set 1: 20 24   9 17    11 18   23 33
  Set 2: 25 33   22 26   28 30   39 40
  Set 3: 34 35   35 36   37 41   47 48

After sorting columns:
  Set 0: 3 13    2 7     2 10    8 16
  Set 1: 20 24   9 17    11 18   23 33
  Set 2: 25 33   22 26   28 30   39 40
  Set 3: 34 35   35 36   37 41   47 48

(Each column is sorted: col0: 3,20,25,34; col1: 2,9,22,35; etc.)
"""
import sys
import glob
from optparse import OptionParser

parser = OptionParser()

parser.add_option(
    "-i",
    "--input_pattern",
    dest="input_pattern",
    help="Input pattern for .set files (e.g., 'sets/*.set' or 'set1.set set2.set')",
    default="C:/Users/Luciano Carvalho/Documents/Projects/Research/nway/data/set/*.set",
)

parser.add_option(
    "-o",
    "--output",
    dest="output_file",
    help="Output combined file (default: stdout)",
    default="C:/Users/Luciano Carvalho/Documents/Projects/Research/nway/data/results_set/combined.set",
)

parser.add_option(
    "-s",
    "--sort",
    dest="sort_columns",
    action="store_true",
    help="Sort intervals by column position across sets (default: False, just combine)",
    default=False,
)

(options, args) = parser.parse_args()

# Get all matching files
if "*" in options.input_pattern or "?" in options.input_pattern:
    files = sorted(glob.glob(options.input_pattern))
else:
    # Treat as space-separated list of files
    files = options.input_pattern.split()

if not files:
    sys.stderr.write(
        "Error: No files found matching pattern: %s\n" % options.input_pattern
    )
    sys.exit(1)

# Read all sets
sets = []
max_intervals = 0

for file_name in files:
    try:
        with open(file_name, "r") as f:
            line = f.read().strip()
            if line:
                intervals = []
                for interval_str in line.split("\t"):
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
    except IOError as e:
        sys.stderr.write("Warning: Could not read %s: %s\n" % (file_name, e))

if not sets:
    sys.stderr.write("Error: No valid sets found\n")
    sys.exit(1)

# If sort_columns is enabled, sort each column across sets
if options.sort_columns:
    # Transpose: group intervals by column position
    columns = []
    for col_idx in range(max_intervals):
        column = []
        for set_idx, intervals in enumerate(sets):
            if col_idx < len(intervals):
                column.append((set_idx, intervals[col_idx]))
        # Sort this column by start position
        column.sort(key=lambda x: x[1][0])
        columns.append(column)

    # Reconstruct sets from sorted columns
    # Find max number of sets needed
    max_sets = max(len(col) for col in columns) if columns else len(sets)

    # Initialize new sets
    new_sets = [[] for _ in range(max_sets)]

    # Distribute sorted intervals back to sets
    for col_idx, column in enumerate(columns):
        for new_set_idx, (original_set_idx, interval) in enumerate(column):
            if new_set_idx < len(new_sets):
                new_sets[new_set_idx].append(interval)

    sets = new_sets

# Open output file or use stdout
if options.output_file:
    # Create output directory if it doesn't exist
    import os

    output_dir = os.path.dirname(options.output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    out = open(options.output_file, "w")
else:
    out = sys.stdout

# Write each set as one line
for intervals in sets:
    if intervals:
        # Format: "start end\tstart end\t..."
        line = "\t".join([f"{start} {end}" for start, end in intervals])
        out.write(line + "\n")

if options.output_file:
    out.close()
    sys.stderr.write("Combined %d set files into %s" % (len(sets), options.output_file))
    if options.sort_columns:
        sys.stderr.write(" (with column sorting)")
    sys.stderr.write("\n")
else:
    sys.stderr.write("Combined %d set files" % len(sets), file=sys.stderr)
    if options.sort_columns:
        sys.stderr.write(" (with column sorting)", file=sys.stderr)
    sys.stderr.write("\n", file=sys.stderr)
