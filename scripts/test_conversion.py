#!/usr/bin/env python
"""
Test script to demonstrate the conversion between formats.
"""
import sys
import tempfile
import os

# Example nway format (each line is a set)
nway_input = """100 200	300 400	500 600
150 250	350 450
180 220	380 420"""

print("=== NWAY FORMAT (Input) ===")
print(nway_input)
print()

# Write to temp file
with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.set') as f:
    f.write(nway_input)
    temp_input = f.name

try:
    # Convert to columnar
    print("=== Converting to COLUMNAR FORMAT ===")
    os.system(f'python scripts/convert_set_to_columnar.py -i {temp_input} -o temp_columnar.csv')
    
    print("\n=== COLUMNAR FORMAT (Output) ===")
    with open('temp_columnar.csv', 'r') as f:
        print(f.read())
    
    # Convert back
    print("\n=== Converting back to NWAY FORMAT ===")
    os.system(f'python scripts/convert_columnar_to_set.py -i temp_columnar.csv -o temp_nway_back.set')
    
    print("\n=== NWAY FORMAT (Round-trip) ===")
    with open('temp_nway_back.set', 'r') as f:
        print(f.read())
    
    # Cleanup
    os.unlink(temp_input)
    if os.path.exists('temp_columnar.csv'):
        os.unlink('temp_columnar.csv')
    if os.path.exists('temp_nway_back.set'):
        os.unlink('temp_nway_back.set')
        
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    if os.path.exists(temp_input):
        os.unlink(temp_input)

