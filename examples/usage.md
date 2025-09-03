# pdf2csv Usage Examples

This file contains practical examples of how to use the pdf2csv script.

## Basic Usage

### Convert a single PDF file
```bash
./pdf2csv.py bank_statement_january.pdf
```
This will create `bank_statement_january.txt` and `bank_statement_january.csv`.

### Convert multiple PDF files
```bash
./pdf2csv.py statement1.pdf statement2.pdf statement3.pdf
```

### Convert all PDF files in the current directory
```bash
./pdf2csv.py *.pdf
```

## Advanced Usage

### Merge multiple files into one CSV
```bash
./pdf2csv.py --merge yearly_statements.csv jan.pdf feb.pdf mar.pdf
```

### Get help
```bash
./pdf2csv.py --help
```

### Check version
```bash
./pdf2csv.py --version
```

## Expected File Structure

After running the script on `bank_statement.pdf`, you'll have:
- `bank_statement.pdf` (original)
- `bank_statement.txt` (extracted text)
- `bank_statement.csv` (converted CSV)

## Note on CSV Format

The current implementation creates a basic CSV with the following columns:
- Date
- Description  
- Amount
- Balance

The actual parsing logic needs to be customized based on your specific bank statement format. This is part of the "vibe coding" approach - the parsing will evolve based on the actual data encountered.
