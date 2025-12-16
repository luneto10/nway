import sys
import glob

def parse_set_line(filepath):
    """
    Parses your flattened set file.
    Format: "start end\tstart end..."
    """
    intervals = []
    try:
        with open(filepath, 'r') as f:
            line = f.read().strip()
            if not line:
                return []
            
            pairs = line.split('\t')
            for p in pairs:
                parts = p.split()
                if len(parts) == 2:
                    intervals.append((int(parts[0]), int(parts[1])))
    except Exception as e:
        sys.stderr.write(f"Error reading {filepath}: {e}\n")
        sys.exit(1)
        
    return intervals

def intersect_two_lists(set_a, set_b):
    """
    The O(N) Two Pointer logic you already have.
    """
    i = 0
    j = 0
    result = []
    
    while i < len(set_a) and j < len(set_b):
        lo = max(set_a[i][0], set_b[j][0])
        hi = min(set_a[i][1], set_b[j][1])
        
        if lo <= hi:
            result.append((lo, hi))
        
        if set_a[i][1] < set_b[j][1]:
            i += 1
        else:
            j += 1
    return result

# --- Main Execution ---

# 1. Get all .set files in the current directory (or a specific path)
# Change '*.set' to match your actual file naming convention
files = sorted(glob.glob('/Users/luneto10/Documents/Projects/Research/nway/data/set/*.set'))

if len(files) < 2:
    print("Error: Need at least 2 .set files to perform intersection.")
    sys.exit(1)

print(f"Intersecting {len(files)} files...", file=sys.stderr)

# 2. Load the first file as the "Current Candidate"
current_intersection = parse_set_line(files[0])

# 3. Iteratively intersect with the rest
for next_file in files[1:]:
    # If we already have 0 regions left, we can stop early (optimization)
    if not current_intersection:
        break
        
    next_data = parse_set_line(next_file)
    current_intersection = intersect_two_lists(current_intersection, next_data)

# 4. Output the final result
output_strings = [f"{r[0]} {r[1]}" for r in current_intersection]
print("\t".join(output_strings))