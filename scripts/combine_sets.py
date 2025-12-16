#!/usr/bin/env python
"""
Combine multiple .set files into a single file for nway input.

Each .set file should contain a single line with tab-separated intervals.
The output file will have one line per input file, where each line represents one set.
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
    default="*.set",
)

parser.add_option(
    "-o",
    "--output",
    dest="output_file",
    help="Output combined file (default: stdout)",
    default=None,
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

# Open output file or use stdout
if options.output_file:
    out = open(options.output_file, "w")
else:
    out = sys.stdout

# Read each set file and write as one line
for file_name in files:
    try:
        with open(file_name, "r") as f:
            line = f.read().strip()
            if line:  # Only write non-empty lines
                out.write(line + "\n")
    except IOError as e:
        sys.stderr.write("Warning: Could not read %s: %s\n" % (file_name, e))

if options.output_file:
    out.close()
    sys.stderr.write(
        "Combined %d set files into %s\n" % (len(files), options.output_file)
    )
else:
    sys.stderr.write("Combined %d set files\n" % len(files), file=sys.stderr)
