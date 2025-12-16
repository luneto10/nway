# Scripts Directory

This directory contains utility scripts for working with nway interval intersection algorithms.

## Directory Structure

### `convert/`
Format conversion scripts:
- **nway_to_columnar.py** - Convert nway format (line-per-set) to columnar CSV/TSV
- **columnar_to_nway.py** - Convert columnar CSV/TSV to nway format (line-per-set)
- **peak_to_set.py** - Convert BED/broadPeak files to .set format
- **bed_to_set.py** - Convert BED files to .set format
- **set_to_bed.py** - Convert .set files back to BED format

### `utils/`
General utility scripts:
- **combine_sets.py** - Combine multiple .set files into one file
- **combine_sets_sorted.py** - Combine sets with optional column sorting
- **merge_contained.py** - Merge contained intervals
- **get_subsets.py** - Extract subsets from interval sets
- **transpose.py** - Transpose tab-separated data

### `validation/`
Validation and checking scripts:
- **check_contain.py** - Check for contained intervals within sets
- **check_intersects.py** - Verify intersections between sets
- **check_sort.py** - Verify intervals are sorted within sets
- **verify_set_columns.py** - Verify column-wise sorting across sets

### `plotting/`
Plotting and visualization scripts for performance analysis.

### `DnaseI/`, `wgEncodeHaibTfbs/`, `wgEncodeUwTfbs/`
Dataset-specific scripts for processing ENCODE data.

## Quick Start

### Convert BED files to nway format:
```bash
python scripts/convert/peak_to_set.py -g data/hg19.genome -b "*.broadPeak" > output.set
```

### Combine multiple set files:
```bash
python scripts/utils/combine_sets.py -i "sets/*.set" -o combined_sets.txt
```

### Convert nway format to columnar format (for your Python code):
```bash
python scripts/convert/nway_to_columnar.py -i combined_sets.txt -o output.csv
```

### Verify combined sets:
```bash
python scripts/validation/verify_set_columns.py -f combined_sets.txt
```

## Format Descriptions

### Nway Format (line-per-set)
Each line represents one set, with tab-separated intervals:
```
100 200	300 400	500 600
150 250	350 450
180 220	380 420
```

### Columnar Format (row-per-interval)
Each row represents one interval across all sets:
```
start_0,end_0,start_1,end_1,start_2,end_2
100,200,150,250,180,220
300,400,350,450,380,420
500,600,,,
```

