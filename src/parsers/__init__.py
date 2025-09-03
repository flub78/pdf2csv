"""
Parser modules for different bank statement formats.

This package contains parsers for extracting structured data
from bank statement text files.
"""

from .base_parser import BaseStatementParser, GenericTextParser
from .specific_parsers import FrenchBankParser

__all__ = ['BaseStatementParser', 'GenericTextParser', 'FrenchBankParser']
