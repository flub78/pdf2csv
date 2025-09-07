#!/usr/bin/env python3

import sys
sys.path.append('/home/frederic/git/pdf2csv/src')

from parsers.sg_parser import SocieteGeneraleParser

# Test the SG parser
parser = SocieteGeneraleParser('/home/frederic/git/pdf2csv/examples/releve_CM_07_2025.txt')
statement = parser.parse()

print(f"Bank: {statement.bank_name}")
print(f"Account: {statement.account_number}")
print(f"Period: {statement.start_date} to {statement.end_date}")
print(f"Transactions: {len(statement.transactions)}")

# Show first few transactions
for i, transaction in enumerate(statement.transactions[:3]):
    print(f"\nTransaction {i+1}:")
    print(f"  Date: {transaction.date}")
    print(f"  Type: {transaction.operation_type}")
    print(f"  Description: {transaction.description[:100]}...")
    print(f"  Debit: {transaction.debit}")
    print(f"  Credit: {transaction.credit}")
