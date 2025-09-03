# pdf2csv

A Python script to convert PDF bank statements into CSV files.

## Purpose

This project provides a Python utility to extract financial data from PDF bank statements and convert them into structured CSV files for easier analysis and processing. It's designed to help users process their bank statements programmatically rather than manually entering transaction data.

## Platform Requirements

The script is intended to run on Linux systems where `pdftotext` is available. The `pdftotext` utility is part of the Poppler PDF rendering library and is commonly available through package managers:

```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# CentOS/RHEL/Fedora
sudo yum install poppler-utils
```

## Experimental Aspect: Vibe Coding

This project serves as an experiment in the "vibe coding" concept - a development approach that emphasizes:

- **Intuitive Development**: Following the natural flow and "feel" of the code rather than rigid architectural patterns
- **Iterative Refinement**: Building functionality through continuous small improvements based on immediate feedback
- **Context-Aware Coding**: Writing code that responds to the specific needs and characteristics of the data being processed
- **Minimal Ceremony**: Focusing on solving the actual problem with minimal boilerplate and over-engineering

The vibe coding approach allows for more organic development where the code structure emerges naturally from the problem domain rather than being imposed by predetermined patterns.

## Usage

The main script is `pdf2csv.py` which provides a command-line interface for converting PDF bank statements to CSV files.

### Prerequisites

Ensure `pdftotext` is installed on your Linux system:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# CentOS/RHEL/Fedora
sudo yum install poppler-utils
```

### Basic Usage

```bash
# Convert a single file
./pdf2csv.py bank_statement.pdf

# Convert multiple files
./pdf2csv.py statement1.pdf statement2.pdf statement3.pdf

# Convert all PDF files in current directory
./pdf2csv.py *.pdf

# Merge multiple files into one CSV
./pdf2csv.py --merge combined.csv *.pdf

# Get help
./pdf2csv.py --help

# Check version
./pdf2csv.py --version
```

### Output

For each PDF file processed, the script creates:
- A `.txt` file containing the extracted text
- A `.csv` file with the converted data

The CSV format includes columns for Date, Description, Amount, and Balance. The parsing logic is designed to be customized based on your specific bank statement format, following the vibe coding approach of iterative refinement.

## Contributing

This is an experimental project. Contributions and feedback on both the functionality and the vibe coding approach are welcome.

## License

MIT License - see LICENSE file for details.
