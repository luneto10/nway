#!/usr/bin/env python
import sys
import numpy as np
import glob
from optparse import OptionParser

parser = OptionParser()

parser.add_option("-g", "--genome_file", dest="genome_file", help="Genome file")

parser.add_option(
    "-b", "--bed_files", dest="bed_files", help="BED files, can have wildcards"
)

(options, args) = parser.parse_args()

if not options.genome_file:
    parser.error("Genome file not given")

if not options.bed_files:
    parser.error("BED files not given")

offsets = {}
offset = 0

# Read genome file robustly (handles tabs/spaces, skips empty lines)
with open(options.genome_file, "r") as f:
    for l in f:
        if not l.strip():
            continue
        # split() without argument splits on any whitespace (space/tab)
        a = l.strip().split()
        if len(a) < 2:
            continue
        chrom = a[0].strip()
        try:
            size = int(a[1])
        except ValueError:
            continue
        offsets[chrom] = offset
        offset += size

# Convert each BED/broadPeak file to .set format
for file_name in glob.glob(options.bed_files):
    with open(file_name, "r") as f:
        line = []
        for l in f:
            if not l.strip():
                continue
            a = l.strip().split()
            if len(a) < 3:
                continue

            chrom = a[0].strip()

            # Map chrM to chrMT if genome file uses chrMT
            if chrom == "chrM" and "chrMT" in offsets:
                chrom = "chrMT"

            if chrom not in offsets:
                # Skip chromosomes that are not in the genome_file
                sys.stderr.write(
                    f"Warning: chromosome {chrom} not in genome file, skipping line\n"
                )
                continue

            try:
                start = int(a[1])
                end = int(a[2])
            except ValueError:
                continue

            base_offset = offsets[chrom]
            # Convert to linear coordinates: BED end is exclusive, so subtract 1
            line.append([start + base_offset, end + base_offset - 1])

    # Sort and print as a single line with tab-separated interval pairs
    l_s = sorted(line)
    print("\t".join([f"{x[0]} {x[1]}" for x in l_s]))
