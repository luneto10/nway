# Validation Scripts

Scripts for checking and validating interval set files.

## check_contain.py
Check for contained/overlapping intervals within a single set.

Usage:
```bash
python scripts/validation/check_contain.py -b input.bed
```

## check_intersects.py
Verify intersections between sets using an intersect file.

Usage:
```bash
python scripts/validation/check_intersects.py -i intersect_file.txt -s sets_file.txt
```

## check_sort.py
Verify that intervals within each set are sorted.

Usage:
```bash
python scripts/validation/check_sort.py input.set
```

## verify_set_columns.py
Verify if intervals at the same column position across sets are sorted.

Usage:
```bash
python scripts/validation/verify_set_columns.py -f combined_sets.txt
```

