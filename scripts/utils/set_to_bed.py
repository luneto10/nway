#!/usr/bin/env python3
import glob
import os
from optparse import OptionParser
from typing import Dict, List, Tuple


def load_genome(genome_path: str) -> Tuple[List[int], Dict[int, str]]:
    """
    Load a genome file of the form:
        chr1 <size>
        chr2 <size>
        ...

    Returns:
    - sorted_offsets: sorted list of chromosome starting offsets (linear coordinates)
    - offset_to_chrom: mapping offset -> chromosome name
    """
    offsets: Dict[str, int] = {}
    offset = 0

    with open(genome_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            chrom = parts[0].strip()
            try:
                size = int(parts[1])
            except ValueError:
                continue
            offsets[chrom] = offset
            offset += size

    offset_to_chrom: Dict[int, str] = {off: ch for ch, off in offsets.items()}
    sorted_offsets: List[int] = sorted(offset_to_chrom.keys())
    return sorted_offsets, offset_to_chrom


def find_chrom_for_position(
    pos: int,
    sorted_offsets: List[int],
    offset_to_chrom: Dict[int, str],
) -> Tuple[str, int]:
    """
    Given a linear coordinate `pos`, find the chromosome and its starting offset.

    We assume chromosomes were concatenated in the same order as in the genome file.
    """
    lo, hi = 0, len(sorted_offsets)

    # Find last index idx such that sorted_offsets[idx] <= pos
    while lo < hi:
        mid = (lo + hi) // 2
        if sorted_offsets[mid] <= pos:
            lo = mid + 1
        else:
            hi = mid
    idx = lo - 1

    if idx < 0:
        raise ValueError(f"Position {pos} is before the first chromosome offset")

    chrom_offset = sorted_offsets[idx]
    chrom = offset_to_chrom[chrom_offset]
    return chrom, chrom_offset


def convert_set_file_to_bed(
    set_path: str,
    bed_path: str,
    sorted_offsets: List[int],
    offset_to_chrom: Dict[int, str],
) -> None:
    """
    Convert a single .set file into a BED file.

    For each "start end" pair (in linear coordinates), we emit:
        chrom  chrom_start  chrom_end
    """
    with open(set_path, "r") as fin, open(bed_path, "w") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            # Each field is "start end", separated by tabs
            fields = [field for field in line.split("\t") if field]
            for field in fields:
                parts = field.strip().split()
                if len(parts) != 2:
                    # Skip any non "start end" tokens (e.g. header path)
                    continue
                try:
                    start = int(parts[0])
                    end = int(parts[1])
                except ValueError:
                    continue

                chrom, chrom_offset = find_chrom_for_position(
                    start, sorted_offsets, offset_to_chrom
                )
                chrom_start = start - chrom_offset
                chrom_end = end - chrom_offset + 1  # BED end is exclusive

                fout.write(f"{chrom}\t{chrom_start}\t{chrom_end}\n")


def set_to_bed_for_all(
    genome_path: str,
    set_pattern: str,
    output_dir: str | None = None,
) -> None:
    """
    Convert all .set files matching `set_pattern` to individual BED files.

    By default, each .bed is written next to its .set:
        /path/foo.set -> /path/foo.bed

    If output_dir is given, all BED files are written there, keeping basenames.
    """
    sorted_offsets, offset_to_chrom = load_genome(genome_path)

    set_paths = sorted(glob.glob(set_pattern))
    if not set_paths:
        print(f"No .set files found for pattern: {set_pattern}")
        return

    for set_path in set_paths:
        base_name = os.path.splitext(os.path.basename(set_path))[0]
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            bed_path = os.path.join(output_dir, base_name + ".bed")
        else:
            folder = os.path.dirname(set_path)
            bed_path = os.path.join(folder, base_name + ".bed")

        print(f"Converting {set_path} -> {bed_path}")
        convert_set_file_to_bed(set_path, bed_path, sorted_offsets, offset_to_chrom)


if __name__ == "__main__":
    parser = OptionParser()

    parser.add_option(
        "-g",
        "--genome_file",
        dest="genome_file",
        help="Genome file, e.g. /Users/.../hg19.genome",
    )

    parser.add_option(
        "-s",
        "--set_files",
        dest="set_files",
        help="Glob pattern for .set files, e.g. '/Users/.../set/*.set'",
    )

    parser.add_option(
        "-o",
        "--output_dir",
        dest="output_dir",
        help="Optional output directory for .bed files (defaults to same dir as .set)",
    )

    (options, args) = parser.parse_args()

    genome_file = (
        options.genome_file
        or "/Users/luneto10/Documents/Projects/Research/nway/data/hg19.genome"
    )
    set_pattern = (
        options.set_files
        or "/Users/luneto10/Documents/Projects/Research/nway/data/set/*.set"
    )
    output_dir = options.output_dir

    set_to_bed_for_all(genome_file, set_pattern, output_dir)
