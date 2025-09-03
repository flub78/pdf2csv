# Parser Usage Examples

This document shows how to use the parser system directly in Python code.

## Basic Parser Usage

```python
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path('.') / 'src'))

from parsers import GenericTextParser, FrenchBankParser
from models import BankStatement

# Parse a text file extracted from PDF
parser = GenericTextParser('statement.txt')
statement = parser.parse()

# Access extracted information
print(f"Bank: {statement.bank_name}")
print(f"Account: {statement.account_number}")
print(f"Period: {statement.get_date_range_str()}")
print(f"Transactions: {statement.get_transaction_count()}")

# Access individual transactions
for transaction in statement.transactions:
    print(f"{transaction.date}: {transaction.description} - {transaction.amount}")

# Export to CSV data
csv_data = statement.to_csv_data()
```

## Using Specific Parsers

```python
# For French bank statements
french_parser = FrenchBankParser('releve_bancaire.txt')
french_statement = french_parser.parse()

# French parser handles:
# - French date formats (DD/MM/YYYY, DD mois YYYY)
# - Euro currency formatting (1 000,00 €)
# - French bank names (Crédit Agricole, BNP Paribas, etc.)
```

## Creating Custom Parsers

```python
from parsers.base_parser import BaseStatementParser

class MyBankParser(BaseStatementParser):
    def parse(self):
        # Custom parsing logic here
        self._extract_bank_info()
        self._extract_transactions()
        return self.statement
    
    def _extract_bank_info(self):
        # Extract bank-specific information
        pass
    
    def _extract_transactions(self):
        # Extract transactions in bank-specific format
        pass
```

## CSV Output

The parser system generates structured CSV with these columns:
- Date
- Description
- Amount
- Balance
- Reference
- Category

This provides much more structured data than the basic text-to-CSV conversion.
