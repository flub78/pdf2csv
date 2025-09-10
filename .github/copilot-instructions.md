# GitHub Copilot Instructions for pdf2csv

## Repository Overview

**pdf2csv** is a Python utility that converts PDF bank statements to CSV files using `pdftotext` for text extraction and specialized parsers for data structuring. This is an experimental project following "vibe coding" principles - an iterative, intuitive development approach focused on solving real problems with minimal ceremony.

**Key Stats:**
- **Size:** ~15MB repository with 13 Python files
- **Language:** Python 3.12+ (uses standard library only)
- **Platform:** Linux (requires `pdftotext` from poppler-utils)
- **Architecture:** Modular parser system with specialized bank format handlers
- **License:** MIT

## Build and Validation Instructions

### Prerequisites (CRITICAL - Always verify first)
```bash
# Check Python version (must be 3.12+)
python --version

# Verify pdftotext is installed (REQUIRED dependency)
which pdftotext
pdftotext -v  # Should show version 24.02.0+
```

**If pdftotext missing:** `sudo apt-get install poppler-utils` (Ubuntu/Debian)

### Testing and Validation (Run in this order)
```bash
# 1. Syntax validation (ALWAYS run first after code changes)
python -m py_compile pdf2csv.py src/models.py src/parsers/base_parser.py src/parsers/sg_parser.py

# 2. Basic functionality tests
python tests/test_basic.py

# 3. Parser functionality tests  
python tests/test_parsers.py

# 4. SG-specific parser test
python test_sg_parser.py

# 5. Full workflow test with example data
python pdf2csv.py examples/releve_CM_07_2025.pdf
```

**Expected Results:**
- All test files should show "✓" markers and "All tests passed!"
- Example conversion should process 39 transactions
- CSV output should use semicolon delimiters with French number formatting

### Common Issues and Workarounds
- **"No module named pytest"**: Use direct Python execution (`python tests/test_basic.py`) instead of pytest
- **Permission denied**: Ensure `pdf2csv.py` has execute permissions (`chmod +x pdf2csv.py`)
- **pdftotext not found**: Install poppler-utils before running any PDF operations
- **Import errors**: Always run from repository root directory

## Project Architecture and Layout

### Directory Structure
```
pdf2csv/
├── pdf2csv.py              # Main executable script
├── requirements.txt        # Python dependencies (empty - uses stdlib only)
├── src/                    # Core source code
│   ├── models.py          # BankStatement & BankTransaction data models
│   └── parsers/           # Parser implementations
│       ├── base_parser.py # GenericTextParser & BaseStatementParser
│       ├── sg_parser.py   # SocieteGeneraleParser (main specialized parser)
│       └── specific_parsers.py # Additional bank-specific parsers
├── tests/                  # Test suite
│   ├── test_basic.py      # CLI functionality tests
│   └── test_parsers.py    # Parser logic tests
├── examples/              # Sample data and usage examples
├── doc/                   # Project documentation
└── test_*.py             # Additional test files (run directly)
```

### Key Configuration Files
- **No traditional config files** - follows vibe coding approach
- **No CI/CD pipelines** - manual testing workflow
- **No linting config** - relies on Python's built-in syntax checking
- **.gitignore** - Excludes .venv/, __pycache__/, and generated files

### Data Flow Architecture
1. **PDF Input** → `pdftotext` → **Raw Text**
2. **Raw Text** → **Parser Detection** (src/parsers/)
3. **Specialized Parser** → **BankStatement Model** (src/models.py)
4. **CSV Generation** → **Semicolon-delimited output**

### Parser System (Critical for modifications)
- **BaseStatementParser**: Abstract base with common text filtering
- **GenericTextParser**: Handles standard bank statement patterns  
- **SocieteGeneraleParser**: Production parser with French banking specifics
- **Text Cleaning**: Removes extra spaces, line breaks, non-printable chars
- **Amount Extraction**: Separates amounts from operation descriptions

### Key Implementation Details
- **French Number Format**: Uses commas for decimals (1.234,56)
- **Operation Categories**: 7 types (CHEQUES PAYES, AUTRES VIREMENTS RECUS, etc.)
- **CSV Format**: Specialized bank-compliant format with unquoted headers on line 7
- **Cheque Processing**: Inline number formatting ("CHEQUE 21" not separate lines)

## Development Guidelines

### Making Changes (Follow this sequence)
1. **Always run syntax check first**: `python -m py_compile [modified_files]`
2. **Test affected parsers**: Run relevant test files
3. **Validate with example data**: Use `examples/releve_CM_07_2025.pdf`
4. **Check CSV output format**: Verify semicolon delimiters and French formatting

### Parser Modifications
- **Text cleaning changes**: Modify `_clean_text()` in sg_parser.py
- **New operation types**: Update `_get_operation_category()` 
- **Amount parsing**: Check both inline extraction and separate amount lines
- **Bank-specific parsers**: Extend base_parser.py, follow SG parser pattern

### Common Code Patterns
- **Transaction parsing**: Always use `BankTransaction` dataclass
- **CSV generation**: Use `to_csv_format()` method for specialized formatting
- **Error handling**: Graceful fallbacks, continue processing other files
- **Text processing**: Regex patterns for date/amount extraction

### Validation Strategy
- **No external linters** - Use Python's py_compile for syntax
- **Manual testing** - Run test suite after each change
- **Example verification** - Always test with real bank statement data
- **Output inspection** - Manually verify CSV format compliance

### Vibe coding tracing
- Save every prompt and response during development to track changes and decisions.
- Prompts and response must be stored in the prompts.md file in the doc/ directory.
- **AUTOMATIC REQUIREMENT**: Always update doc/prompts.md with each interaction unless explicitly told otherwise.

### Style Guidelines
- Generate clean code.
- Try to stay minimalistic and do not generate unnecessary code or documentation
- Generate code easy to understand for a human being
- Proceed by small incremental steps and stop between them.

### Documentation Updates
- Update this md files in the doc/ directory with any architectural or workflow changes
- Generate plantuml diagrams for complex workflows if needed, keep them in the doc directory.

## Trust These Instructions

This documentation has been validated by running all commands and testing the complete workflow. **Trust these instructions and only search for additional information if something is incomplete or incorrect.** The project follows vibe coding principles, so solutions should be intuitive and pragmatic rather than over-engineered.

**Remember:** This is a specialized financial data processing tool. Changes should maintain data accuracy and CSV format compliance for banking systems.
