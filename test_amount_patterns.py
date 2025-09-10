#!/usr/bin/env python3
"""
Test script to verify improved amount patterns can handle large amounts
"""

import re

# New improved patterns
improved_patterns = [
    # Formatted amounts (with thousand separators): 1,234.56 or 1.234,56
    r'[\$€£¥]?\s*([+-]?\d{1,3}(?:[,\s]\d{3})+(?:[.,]\d{2})?)',
    r'([+-]?\d{1,3}(?:[,\s]\d{3})+(?:[.,]\d{2})?)\s*[\$€£¥]?',
    # Unformatted amounts (no separators): 1234567.89 or 1234567,89
    r'[\$€£¥]?\s*([+-]?\d{4,}(?:[.,]\d{2})?)',
    r'([+-]?\d{4,}(?:[.,]\d{2})?)\s*[\$€£¥]?',
    # Small amounts (1-999): 123.45 or 123,45
    r'[\$€£¥]?\s*([+-]?\d{1,3}(?:[.,]\d{2})?)',
    r'([+-]?\d{1,3}(?:[.,]\d{2})?)\s*[\$€£¥]?'
]

# French improved pattern
french_pattern = r'(\d{1,3}(?:\.\d{3})+(?:,\d{2})?|\d{4,}(?:,\d{2})?|\d{1,3}(?:,\d{2})?)'

# Test cases that should work with new patterns
test_amounts = [
    # Large amounts that failed before
    "5000000,00",      # 5 million unformatted
    "25000000.00",     # 25 million unformatted
    "12345,67",        # 12K unformatted
    "€ 5000000,00",    # 5 million with currency
    "$ 25000000.00",   # 25 million with currency
    
    # Formatted amounts (should still work)
    "1.234.567,89",    # French format
    "1,234,567.89",    # US format
    "€ 1.234.567,89",  # French with currency
    "$ 1,234,567.89",  # US with currency
    
    # Small amounts (should still work)
    "123,45",          # Small French
    "123.45",          # Small US
    "€ 123,45",        # Small with currency
]

print("Testing improved amount patterns...")
print("=" * 50)

for amount in test_amounts:
    found = False
    matched_pattern = None
    extracted_value = None
    
    # Test against improved patterns
    for i, pattern in enumerate(improved_patterns):
        match = re.search(pattern, amount)
        if match:
            found = True
            matched_pattern = f"Pattern {i+1}"
            extracted_value = match.group(1)
            break
    
    # Test against French pattern
    if not found:
        match = re.search(french_pattern, amount)
        if match:
            found = True
            matched_pattern = "French pattern"
            extracted_value = match.group(1)
    
    status = "✅ PASS" if found else "❌ FAIL"
    print(f"{status} '{amount}' -> {matched_pattern}: '{extracted_value}'" if found else f"{status} '{amount}' -> No match")

print("\n" + "=" * 50)
print("Testing complete!")
