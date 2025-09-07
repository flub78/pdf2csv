"""
Base parser class and utilities for bank statement parsing.

This module provides the foundation for parsing different bank statement formats.
Following the vibe coding approach, parsers can be customized and extended
based on actual data encountered.
"""

import re
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple
import sys
import os

# Add src directory to path for models import
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(current_dir)
sys.path.append(src_dir)

from models import BankStatement, BankTransaction


class BaseStatementParser(ABC):
    """Abstract base class for bank statement parsers."""
    
    def __init__(self, text_file_path: str):
        """
        Initialize parser with text file path.
        
        Args:
            text_file_path: Path to the text file extracted from PDF
        """
        self.text_file_path = Path(text_file_path)
        self.raw_text = ""
        self.lines = []
        self.statement = BankStatement()
        
        if not self.text_file_path.exists():
            raise FileNotFoundError(f"Text file not found: {text_file_path}")
        
        self._load_text()
    
    def _load_text(self):
        """Load text content from file."""
        try:
            with open(self.text_file_path, 'r', encoding='utf-8') as f:
                self.raw_text = f.read()
            self.lines = self.raw_text.split('\n')
            self.lines = self._filter_ignore_lines(self.lines)
        except Exception as e:
            raise IOError(f"Error reading text file: {e}")
    
    def _filter_ignore_lines(self, lines: List[str]) -> List[str]:
        """Filter out lines that should be ignored during parsing."""
        ignore_patterns = [
            r'VOS CONTACTS',
            r'Votre Banque à Distance',
            r'Internet\s*:\s*entreprises\.sg\.fr',
            r'éléphone\s*:\s*\d+',
            r'Courrier\s*:\s*\d+.*ABBEVILLE',
            r'AERODROME D ABBEVILLE',
            r'Service d\'urgence 24 h/24',
            r'Perte ou vol de vos cartes',
            r'Pour toute insatisfaction',
            r'L\'agence\s*:\s*votre premier',
            r'Le Service Relations Clientèle',
            r'Le Médiateur\s*:\s*En dernier',
            r'Société Générale',
            r'S\.A\. au capital',
            r'RCS Paris',
            r'Siège Social',
            r'bd Haussmann',
            r'suite >>>',
            r'RA\d+',
            r'N° ADEME',
            r'Opération exonérée',
            r'Votre compte est éligible',
            r'Fonds de Garantie',
            r'SG-SocieteGenerale\.Reclamations@socgen\.com',
            r'courrier à : Le médiateur CS 151',
            r'RELEVÉ DE COMPTE',
            r'COMPTE D\'ADMINISTRATION - en euros',
            r'n° 30003 02846 00050034631 54',
            r'du \d{2}/\d{2}/\d{4} au \d{2}/\d{2}/\d{4}',
            r'envoi n°\d+ Page \d+/\d+',
            r'Nature de l\'opération',
            r'^Débit$',
            r'^Crédit$'
        ]
        
        filtered_lines = []
        for line in lines:
            # Stop processing after TOTAUX DES MOUVEMENTS
            if re.search(r'TOTAUX DES MOUVEMENTS', line, re.IGNORECASE):
                break
                
            should_ignore = False
            for pattern in ignore_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    should_ignore = True
                    break
            if not should_ignore:
                filtered_lines.append(line)
        
        return filtered_lines
    
    @abstractmethod
    def parse(self) -> BankStatement:
        """Parse the text file and extract bank statement information."""
        pass
    
    def get_bank_name(self) -> str:
        """Extract bank name from the statement."""
        return self.statement.bank_name
    
    def get_bank_identification(self) -> str:
        """Extract bank identification code."""
        return self.statement.bank_code
    
    def get_start_date(self) -> Optional[datetime]:
        """Extract statement start date."""
        return self.statement.start_date
    
    def get_end_date(self) -> Optional[datetime]:
        """Extract statement end date."""
        return self.statement.end_date
    
    def get_transactions(self) -> List[BankTransaction]:
        """Get collection of bank transactions."""
        return self.statement.transactions
    
    def get_statement(self) -> BankStatement:
        """Get the complete bank statement object."""
        return self.statement


class GenericTextParser(BaseStatementParser):
    """
    Generic parser for bank statements with common patterns.
    
    This parser uses heuristics to extract information from various
    bank statement formats. It can be extended for specific banks.
    """
    
    def __init__(self, text_file_path: str):
        super().__init__(text_file_path)
        
        # Common date patterns
        self.date_patterns = [
            r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b',  # DD/MM/YYYY or MM/DD/YYYY
            r'\b(\d{2,4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2})\b',  # YYYY/MM/DD
            r'\b(\d{1,2}\s+\w{3}\s+\d{2,4})\b',              # DD MMM YYYY
            r'\b(\w{3}\s+\d{1,2},?\s+\d{2,4})\b'             # MMM DD, YYYY
        ]
        
        # Common amount patterns (with currency symbols)
        self.amount_patterns = [
            r'[\$€£¥]?\s*([+-]?\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{2})?)',
            r'([+-]?\d{1,3}(?:[,\s]\d{3})*(?:[.,]\d{2})?)\s*[\$€£¥]?'
        ]
        
        # Common bank name patterns
        self.bank_patterns = [
            r'(?i)\b([A-Z][a-z]+\s+(?:Bank|Credit\s+Union|Financial))\b',
            r'(?i)\b(Bank\s+of\s+[A-Z][a-z]+)\b',
            r'(?i)\b([A-Z]+\s+Bank)\b'
        ]
    
    def parse(self) -> BankStatement:
        """Parse the text file using generic patterns."""
        self._extract_bank_info()
        self._extract_dates()
        self._extract_transactions()
        return self.statement
    
    def _extract_bank_info(self):
        """Extract bank name and identification information."""
        # Look for bank name in first few lines
        for i, line in enumerate(self.lines[:10]):
            line = line.strip()
            if not line:
                continue
                
            # Check for bank name patterns
            for pattern in self.bank_patterns:
                match = re.search(pattern, line)
                if match:
                    self.statement.bank_name = match.group(1).strip()
                    break
            
            # Look for account numbers
            account_match = re.search(r'(?i)account\s*(?:number|#)?\s*:?\s*(\w+[-\s]?\w+)', line)
            if account_match:
                self.statement.account_number = account_match.group(1)
            
            # Look for bank codes
            code_match = re.search(r'(?i)(?:sort\s+code|routing|swift|iban)\s*:?\s*([A-Z0-9\-\s]+)', line)
            if code_match:
                self.statement.bank_code = code_match.group(1).strip()
        
        # If no bank name found, try to extract from filename or use generic
        if not self.statement.bank_name:
            self.statement.bank_name = "Unknown Bank"
    
    def _extract_dates(self):
        """Extract start and end dates from the statement."""
        dates_found = []
        
        # Look for dates in the first 20 lines
        for line in self.lines[:20]:
            for pattern in self.date_patterns:
                matches = re.findall(pattern, line)
                for match in matches:
                    parsed_date = self._parse_date(match)
                    if parsed_date:
                        dates_found.append(parsed_date)
        
        # Set start and end dates
        if dates_found:
            dates_found.sort()
            self.statement.start_date = dates_found[0]
            self.statement.end_date = dates_found[-1]
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats."""
        date_formats = [
            "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d",
            "%d-%m-%Y", "%m-%d-%Y", "%Y-%m-%d",
            "%d.%m.%Y", "%m.%d.%Y", "%Y.%m.%d",
            "%d %b %Y", "%d %B %Y",
            "%b %d, %Y", "%B %d, %Y"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _extract_transactions(self):
        """Extract transactions from the statement."""
        transaction_lines = []
        
        # Simple heuristic: look for lines with dates and amounts
        for line_num, line in enumerate(self.lines):
            line = line.strip()
            if not line:
                continue
            
            # Check if line contains a date
            date_found = None
            for pattern in self.date_patterns:
                match = re.search(pattern, line)
                if match:
                    date_found = self._parse_date(match.group(1))
                    break
            
            if date_found:
                # Look for amounts in the same line
                amounts = self._extract_amounts(line)
                
                # Create transaction
                transaction = BankTransaction()
                transaction.date = date_found
                transaction.description = self._clean_description(line)
                
                if amounts:
                    # Assume last amount is the transaction amount
                    # and second-to-last (if exists) is balance
                    if len(amounts) >= 2:
                        transaction.amount = amounts[-2]
                        transaction.balance = amounts[-1]
                    else:
                        transaction.amount = amounts[0]
                
                self.statement.add_transaction(transaction)
    
    def _extract_amounts(self, line: str) -> List[float]:
        """Extract monetary amounts from a line."""
        amounts = []
        
        for pattern in self.amount_patterns:
            matches = re.findall(pattern, line)
            for match in matches:
                try:
                    # Clean the amount string
                    amount_str = match.replace(',', '').replace(' ', '')
                    amount = float(amount_str)
                    amounts.append(amount)
                except ValueError:
                    continue
        
        return amounts
    
    def _clean_description(self, line: str) -> str:
        """Clean transaction description by removing dates and amounts."""
        cleaned = line
        
        # Remove dates
        for pattern in self.date_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Remove amounts
        for pattern in self.amount_patterns:
            cleaned = re.sub(pattern, '', cleaned)
        
        # Clean up extra spaces
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned if cleaned else "Transaction"
