"""
Specific parsers for different bank statement formats.

This module contains specialized parsers for specific banks,
extending the base parser functionality.
"""

import re
from datetime import datetime
from typing import Optional, List
import sys
import os

# Add paths for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parsers_dir = current_dir
src_dir = os.path.dirname(current_dir)

sys.path.append(src_dir)
sys.path.append(parsers_dir)

from base_parser import BaseStatementParser
from models import BankTransaction, BankStatement


class FrenchBankParser(BaseStatementParser):
    """
    Parser for French bank statements with common format patterns.
    
    This parser recognizes French date formats, currency patterns,
    and common French banking terminology.
    """
    
    def __init__(self, text_file_path: str):
        super().__init__(text_file_path)
        
        # French date patterns
        self.french_date_patterns = [
            r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b',  # DD/MM/YYYY
            r'\b(\d{1,2}\s+(?:janv|févr|mars|avr|mai|juin|juil|août|sept|oct|nov|déc)\w*\.?\s+\d{2,4})\b'
        ]
        
        # French amount patterns (EUR)
        self.french_amount_patterns = [
            r'([+-]?\d{1,3}(?:\s\d{3})*(?:,\d{2})?)\s*€',
            r'([+-]?\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*EUR',
            r'€\s*([+-]?\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{2})?)'
        ]
        
        # French bank name patterns
        self.french_bank_patterns = [
            r'(?i)\b(Crédit\s+(?:Agricole|Mutuel|du\s+Nord|Lyonnais))\b',
            r'(?i)\b(Banque\s+(?:Populaire|Postale|de\s+France))\b',
            r'(?i)\b(BNP\s*Paribas|Société\s+Générale|LCL)\b',
            r'(?i)\b(Caisse\s+d\'Épargne)\b'
        ]
    
    def parse(self) -> BankStatement:
        """Parse French bank statement format."""
        self._extract_french_bank_info()
        self._extract_french_dates()
        self._extract_french_transactions()
        return self.statement
    
    def _extract_french_bank_info(self):
        """Extract French bank information."""
        for line in self.lines[:15]:
            line = line.strip()
            if not line:
                continue
            
            # Check for French bank names
            for pattern in self.french_bank_patterns:
                match = re.search(pattern, line)
                if match:
                    self.statement.bank_name = match.group(1).strip()
                    break
            
            # Look for French account patterns
            account_patterns = [
                r'(?i)compte\s*(?:n°|numéro)?\s*:?\s*(\d+[\s\-]?\d*)',
                r'(?i)n°\s*compte\s*:?\s*(\d+[\s\-]?\d*)',
                r'\b(\d{5,}\s*\d{3,})\b'  # Generic account number pattern
            ]
            
            for pattern in account_patterns:
                match = re.search(pattern, line)
                if match:
                    self.statement.account_number = match.group(1).replace(' ', '')
                    break
        
        if not self.statement.bank_name:
            self.statement.bank_name = "Banque Française"
    
    def _extract_french_dates(self):
        """Extract dates using French formats."""
        dates_found = []
        
        for line in self.lines[:25]:
            for pattern in self.french_date_patterns:
                matches = re.findall(pattern, line, re.IGNORECASE)
                for match in matches:
                    parsed_date = self._parse_french_date(match)
                    if parsed_date:
                        dates_found.append(parsed_date)
        
        if dates_found:
            dates_found.sort()
            self.statement.start_date = dates_found[0]
            self.statement.end_date = dates_found[-1]
    
    def _parse_french_date(self, date_str: str) -> Optional[datetime]:
        """Parse French date formats."""
        # French month abbreviations mapping
        french_months = {
            'janv': 'Jan', 'févr': 'Feb', 'mars': 'Mar', 'avr': 'Apr',
            'mai': 'May', 'juin': 'Jun', 'juil': 'Jul', 'août': 'Aug',
            'sept': 'Sep', 'oct': 'Oct', 'nov': 'Nov', 'déc': 'Dec'
        }
        
        # Convert French month names to English
        normalized_date = date_str.lower()
        for fr_month, en_month in french_months.items():
            if fr_month in normalized_date:
                normalized_date = normalized_date.replace(fr_month, en_month)
                break
        
        date_formats = [
            "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
            "%d/%m/%y", "%d-%m-%y", "%d.%m.%y",
            "%d %b %Y", "%d %B %Y"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(normalized_date.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _extract_french_transactions(self):
        """Extract transactions with French formatting."""
        for line in self.lines:
            line = line.strip()
            if not line or len(line) < 10:
                continue
            
            # Look for date at start of line
            date_found = None
            for pattern in self.french_date_patterns:
                match = re.search(r'^' + pattern, line, re.IGNORECASE)
                if match:
                    date_found = self._parse_french_date(match.group(1))
                    break
            
            if date_found:
                # Extract amounts
                amounts = self._extract_french_amounts(line)
                
                # Create transaction
                transaction = BankTransaction()
                transaction.date = date_found
                transaction.description = self._clean_french_description(line)
                
                if amounts:
                    if len(amounts) >= 2:
                        transaction.amount = amounts[0]
                        transaction.balance = amounts[-1]
                    else:
                        transaction.amount = amounts[0]
                
                self.statement.add_transaction(transaction)
    
    def _extract_french_amounts(self, line: str) -> List[float]:
        """Extract amounts with French formatting (comma as decimal separator)."""
        amounts = []
        
        for pattern in self.french_amount_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                try:
                    # Convert French number format to float
                    # Replace spaces and dots used as thousands separators
                    amount_str = match.replace(' ', '').replace('.', '')
                    # Replace comma decimal separator with dot
                    amount_str = amount_str.replace(',', '.')
                    amount = float(amount_str)
                    amounts.append(amount)
                except ValueError:
                    continue
        
        return amounts
    
    def _clean_french_description(self, line: str) -> str:
        """Clean French transaction description."""
        cleaned = line
        
        # Remove dates
        for pattern in self.french_date_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        # Remove amounts
        for pattern in self.french_amount_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned if cleaned else "Opération"
