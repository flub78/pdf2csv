#!/usr/bin/env python3
"""
Test script for parser functionality.
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

try:
    from parsers import GenericTextParser, FrenchBankParser
    from models import BankStatement, BankTransaction
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


def create_test_text_file(content: str) -> str:
    """Create a temporary text file with test content."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        return f.name


def test_generic_parser():
    """Test the generic parser with sample content."""
    print("Testing Generic Parser...")
    
    sample_content = """
    EXAMPLE BANK
    Account Statement
    Account Number: 123456789
    
    Date: 01/01/2025 to 31/01/2025
    
    01/01/2025  Opening Balance              1000.00
    05/01/2025  ATM Withdrawal    -50.00     950.00
    10/01/2025  Deposit           200.00    1150.00
    15/01/2025  Online Transfer   -75.50    1074.50
    31/01/2025  Closing Balance             1074.50
    """
    
    test_file = create_test_text_file(sample_content)
    
    try:
        parser = GenericTextParser(test_file)
        statement = parser.parse()
        
        print(f"  ✓ Bank Name: {statement.bank_name}")
        print(f"  ✓ Account: {statement.account_number}")
        print(f"  ✓ Date Range: {statement.get_date_range_str()}")
        print(f"  ✓ Transactions: {statement.get_transaction_count()}")
        
        # Display first few transactions
        for i, transaction in enumerate(statement.transactions[:3]):
            print(f"    Transaction {i+1}: {transaction}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ Generic parser failed: {e}")
        return False
    finally:
        os.unlink(test_file)


def test_french_parser():
    """Test the French parser with sample content."""
    print("\nTesting French Parser...")
    
    sample_content = """
    CRÉDIT AGRICOLE
    Relevé de Compte
    N° Compte: 12345 67890
    
    Période du 01/01/2025 au 31/01/2025
    
    01/01/2025  Solde précédent               1 000,00 €
    05/01/2025  Retrait DAB       -50,00 €     950,00 €
    10/01/2025  Virement reçu     200,00 €   1 150,00 €
    15/01/2025  Prélèvement       -75,50 €   1 074,50 €
    31/01/2025  Solde actuel                 1 074,50 €
    """
    
    test_file = create_test_text_file(sample_content)
    
    try:
        parser = FrenchBankParser(test_file)
        statement = parser.parse()
        
        print(f"  ✓ Bank Name: {statement.bank_name}")
        print(f"  ✓ Account: {statement.account_number}")
        print(f"  ✓ Date Range: {statement.get_date_range_str()}")
        print(f"  ✓ Transactions: {statement.get_transaction_count()}")
        
        # Display first few transactions
        for i, transaction in enumerate(statement.transactions[:3]):
            print(f"    Transaction {i+1}: {transaction}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ French parser failed: {e}")
        return False
    finally:
        os.unlink(test_file)


def test_csv_output():
    """Test CSV output format."""
    print("\nTesting CSV Output...")
    
    try:
        # Create a simple statement
        statement = BankStatement()
        statement.bank_name = "Test Bank"
        statement.account_number = "123456"
        
        # Add sample transactions
        from datetime import datetime
        
        transaction1 = BankTransaction()
        transaction1.date = datetime(2025, 1, 1)
        transaction1.description = "Opening Balance"
        transaction1.amount = 1000.00
        transaction1.balance = 1000.00
        
        transaction2 = BankTransaction()
        transaction2.date = datetime(2025, 1, 5)
        transaction2.description = "ATM Withdrawal"
        transaction2.amount = -50.00
        transaction2.balance = 950.00
        
        statement.add_transaction(transaction1)
        statement.add_transaction(transaction2)
        
        # Test CSV output
        csv_data = statement.to_csv_data()
        print(f"  ✓ CSV rows generated: {len(csv_data)}")
        print(f"  ✓ Header: {csv_data[0]}")
        print(f"  ✓ Sample row: {csv_data[1]}")
        
        return True
        
    except Exception as e:
        print(f"  ✗ CSV output test failed: {e}")
        return False


def main():
    """Run parser tests."""
    print("Running parser tests...")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent.parent)
    
    tests = [
        test_generic_parser,
        test_french_parser,
        test_csv_output
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Parser tests passed: {passed}/{total}")
    
    if passed == total:
        print("All parser tests passed! ✓")
        return 0
    else:
        print("Some parser tests failed! ✗")
        return 1


if __name__ == "__main__":
    sys.exit(main())
