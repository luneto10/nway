import csv
import glob
import argparse
from typing import List, Tuple


def parse_set_file(path: str) -> List[Tuple[int, int]]:
    """
    Read a .set file and return a list of (start, end) pairs.

    We assume lines look like:
        1200 1400\t5000 5200\t23000 23500

    Each field is "start end" and fields are separated by tabs.
    Any malformed tokens are skipped defensively.
    """
    intervals: List[Tuple[int, int]] = []

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Each field is "start end", separated by tabs
            fields = [field for field in line.split("\t") if field]
            for field in fields:
                parts = field.strip().split()
                if len(parts) != 2:
                    # Skip malformed chunks
                    continue
                start_str, end_str = parts
                try:
                    start = int(start_str)
                    end = int(end_str)
                except ValueError:
                    # Skip non-integer tokens defensively
                    continue
                intervals.append((start, end))

    return intervals


def sets_to_wide_csv(pattern: str, csv_file: str) -> None:
    """
    Convert multiple .set files into a single wide CSV.

    Each .set file becomes a pair of columns:
        col1_start,col1_end,col2_start,col2_end,...

    col1_* corresponds to the first file matching the glob pattern,
    col2_* to the second, and so on.
    """
    set_paths = sorted(glob.glob(pattern))
    if not set_paths:
        print(f"No files found for pattern: {pattern}")
        return

    # Read all sets into memory
    all_intervals: List[List[Tuple[int, int]]] = []
    for path in set_paths:
        intervals = parse_set_file(path)
        all_intervals.append(intervals)

    # If everything is empty, nothing to write
    if all(len(iv) == 0 for iv in all_intervals):
        print("Warning: no intervals were read from any .set file.")
        return

    max_len = max(len(iv) for iv in all_intervals)

    # Build header: col1_start,col1_end,col2_start,col2_end,...
    header: List[str] = []
    for idx in range(len(all_intervals)):
        col_idx = idx + 1
        header.append(f"col{col_idx}_start")
        header.append(f"col{col_idx}_end")

    with open(csv_file, "w", newline="") as out_f:
        writer = csv.writer(out_f)
        writer.writerow(header)

        # Row i: i-th interval of each set
        for i in range(max_len):
            row: List[str] = []
            for intervals in all_intervals:
                if i < len(intervals):
                    start, end = intervals[i]
                    row.append(str(start))
                    row.append(str(end))
                else:
                    # This set has fewer intervals, pad with empty cells
                    row.append("")
                    row.append("")
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Convert multiple .set files into a wide CSV, "
            "where each set corresponds to one start/end column pair."
        )
    )

    parser.add_argument(
        "-p",
        "--pattern",
        help=(
            "Glob pattern for .set files, "
            "e.g. '/Users/luneto10/Documents/Projects/Research/nway/data/set/*.set'"
        ),
        default="/Users/luneto10/Documents/Projects/Research/nway/data/set/*.set",
    )
    parser.add_argument(
        "-o",
        "--csv-file",
        help="Path to the output .csv file",
        default="/Users/luneto10/Documents/Projects/Research/nway/data/set/wide.csv",
    )

    args = parser.parse_args()
    sets_to_wide_csv(args.pattern, args.csv_file)
