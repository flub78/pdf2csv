#!/usr/bin/env python3

import sys
sys.path.append('/home/frederic/git/pdf2csv/src')

from parsers.sg_parser import SocieteGeneraleParser

# Test the SG parser header generation
parser = SocieteGeneraleParser('/home/frederic/git/pdf2csv/examples/releve_CM_07_2025.txt')
statement = parser.parse()

print("=== Statement Info ===")
print(f"Bank: '{statement.bank_name}'")
print(f"Account: '{statement.account_number}'")
print(f"Bank Code: '{statement.bank_code}'")
print(f"Final Balance: {statement.final_balance}")

print("\n=== CSV Header Lines ===")
csv_rows = parser.to_csv_format()
for i, row in enumerate(csv_rows[:6]):
    print(f"Row {i+1}: {row}")

print("\n=== Expected ===")
expected = [
    ['"SG ABBEVILLE LEJEUNE    "'],
    ['"FR76 3000 3028 4600 0500 3463 154"', '"CM"'],
    ['"CAV ADMI"'],
    ['"Solde au"', '"02/09/2025"'],
    ['"Solde"', '"117 767,32"', '"EUR"']
]
for i, row in enumerate(expected):
    print(f"Expected {i+1}: {row}")
