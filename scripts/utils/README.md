# Utility Scripts

Helper scripts for working with interval sets.

## combine_sets.py
Combine multiple .set files into a single file for nway input.

Each .set file becomes one line in the combined file.

Usage:
```bash
python scripts/utils/combine_sets.py -i "sets/*.set" -o combined_sets.txt
```

## combine_sets_sorted.py
Combine sets with optional column-wise sorting.

Usage:
```bash
# Just combine
python scripts/utils/combine_sets_sorted.py -i "sets/*.set" -o combined_sets.txt

# Combine and sort columns
python scripts/utils/combine_sets_sorted.py -i "sets/*.set" -o combined_sets.txt -s
```

## merge_contained.py
Merge contained intervals within sets.

## get_subsets.py
Extract subsets from interval sets.

## transpose.py
Transpose tab-separated data (simple utility).

