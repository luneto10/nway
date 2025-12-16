# Conversion Scripts

Scripts for converting between different file formats.

## Format Conversions

### nway_to_columnar.py
Convert nway combined set format to columnar CSV/TSV format.

**Input (nway format):** Each line is a set
```
100 200	300 400	500 600
150 250	350 450
180 220	380 420
```

**Output (columnar format):** Each row is one interval across all sets
```
start_0,end_0,start_1,end_1,start_2,end_2
100,200,150,250,180,220
300,400,350,450,380,420
500,600,,,
```

Usage:
```bash
python scripts/convert/nway_to_columnar.py -i combined_sets.txt -o output.csv
```

### columnar_to_nway.py
Convert columnar CSV/TSV format to nway combined set format.

Usage:
```bash
python scripts/convert/columnar_to_nway.py -i input.csv -o combined_sets.txt
```

### peak_to_set.py
Convert BED/broadPeak files to .set format (nway format).

Usage:
```bash
python scripts/convert/peak_to_set.py -g data/hg19.genome -b "*.broadPeak" > output.set
```

### bed_to_set.py
Convert BED files to .set format (nway format).

Usage:
```bash
python scripts/convert/bed_to_set.py -g data/hg19.genome -b "*.bed" > output.set
```

### set_to_bed.py
Convert .set files back to BED format.

Usage:
```bash
python scripts/convert/set_to_bed.py -g data/hg19.genome -s input.set -o output.bed
```

