#!/usr/bin/env python3

from src.parsers.base_parser import GenericTextParser
import tempfile
import os

# Create test file with ignore patterns
test_content = """Transaction line 1
VOS CONTACTS
Another transaction
Société Générale
Real transaction data
Votre Banque à Distance
More transaction data"""

with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
    f.write(test_content)
    temp_file = f.name

print("Original content:")
print(test_content)
print("\nFiltered lines:")

parser = GenericTextParser(temp_file)
for line in parser.lines:
    if line.strip():
        print(f'  "{line}"')

os.unlink(temp_file)
