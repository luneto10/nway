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

# Lê o arquivo de genoma de forma robusta
with open(options.genome_file, "r") as f:
    for l in f:
        if not l.strip():
            continue
        # split() sem argumento quebra em qualquer espaço/tab
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

# Converte cada BED/broadPeak em .set
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

            # Se tiver caso chrM mas o genome usa chrMT, mapeia
            if chrom == "chrM" and "chrMT" in offsets:
                chrom = "chrMT"

            if chrom not in offsets:
                # Ignora cromossomos que não estão no genome_file
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
            line.append([start + base_offset, end + base_offset - 1])

    # Ordena e imprime a linha única com os pares
    l_s = sorted(line)
    print("\t".join([f"{x[0]} {x[1]}" for x in l_s]))
