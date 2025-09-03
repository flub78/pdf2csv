# Project Structure

This document describes the organization of the pdf2csv project.

## Directory Structure

```
pdf2csv/
├── LICENSE                 # MIT License
├── README.md              # Main project documentation
├── pdf2csv.py            # Main script (executable)
├── requirements.txt      # Python dependencies (minimal for this project)
├── src/                  # Source code directory
│   ├── __init__.py      # Package initialization
│   ├── models.py        # Data models (BankStatement, BankTransaction)
│   └── parsers/         # Parser package
│       ├── __init__.py  # Parser package initialization
│       ├── base_parser.py      # Base parser and generic parser
│       └── specific_parsers.py # Specialized parsers (French bank, etc.)
├── doc/                  # Documentation directory
│   ├── prompts.md       # AI prompts used in development
│   └── structure.md     # This file - project structure
├── examples/            # Usage examples and documentation
│   └── usage.md        # Practical usage examples
└── tests/              # Test scripts
    ├── test_basic.py   # Basic functionality tests
    └── test_parsers.py # Parser functionality tests
```

## Key Files

### `pdf2csv.py`
The main executable script that:
- Accepts PDF files as command-line arguments
- Uses `pdftotext` to extract text from PDFs
- Converts text to CSV format
- Supports merging multiple files
- Provides `--help` and `--version` options

### `doc/prompts.md`
Records all AI prompts used in the development process for analysis and reference, supporting the experimental "vibe coding" approach.

### `src/models.py`
Data models for representing bank statements and transactions:
- `BankTransaction`: Individual transaction with date, description, amount, balance
- `BankStatement`: Complete statement with bank info, account details, and transaction collection
- Both include CSV conversion methods

### `src/parsers/`
Parser system for extracting structured data from text files:
- `BaseStatementParser`: Abstract base class for all parsers
- `GenericTextParser`: Handles common bank statement patterns
- `FrenchBankParser`: Specialized for French banking formats
- Extensible architecture for adding new bank-specific parsers

### `tests/test_parsers.py`
Comprehensive test suite for parser functionality, including sample data for different formats.

### `examples/usage.md`
Practical examples showing how to use the script in various scenarios.

## Design Philosophy

The project follows the "vibe coding" experimental approach:
- Clean, intuitive code structure
- Minimal dependencies (only standard library)
- Iterative development based on actual needs
- Context-aware parsing that can be customized
- Organic growth of functionality
