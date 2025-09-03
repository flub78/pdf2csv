# AI Prompts Documentation

This file contains all AI prompts used for this project for further analysis and reference. Each entry includes both the user prompt and the AI response for complete traceability.

---

### 2025-09-03 - Session 1
#### Prompt:
I want to create a python script to convert pdf bank statements into csv files. The script will run on a linux system where pdftotext is available. The project will be also an experiment on the vibe coding concept. Describe this into the Readme.md. Create a doc repository and create a doc/prompts.md file to store the AI prompts for further analysis. Insert this prompt into the doc/prompts.md file as an entry with today date.

#### AI Response:
I created a complete project structure for pdf2csv with:
1. **README.md**: Documented the project purpose, vibe coding concept, platform requirements (Linux with pdftotext), and usage instructions
2. **doc/ directory**: Created with prompts.md to store AI interactions
3. **Project setup**: Established the foundation for a Python script to convert PDF bank statements to CSV
4. **Vibe coding documentation**: Explained the experimental approach emphasizing intuitive development, iterative refinement, context-aware coding, and minimal ceremony

The README describes vibe coding as a development approach that follows the natural flow of code rather than rigid patterns, allowing organic development where structure emerges from the problem domain.

---

### 2025-09-03 - Session 2
#### Prompt:
Create a python script named pdf2csv.py. This script should takes one or several pdf files as input parameters. It should run the pdf2text command on each of these input parameters and create new files with extension .txt. The script should answer to the --help and --version option. It should have a --merge option in order to merge several files into one unique csv file. You should organize the code cleanly, create the required directories. Add every prompt as en entry into doc/prompts.md

#### AI Response:
I created a comprehensive Python script `pdf2csv.py` with the following features:

**Core Functionality:**
- Command-line interface accepting multiple PDF files as parameters
- Runs `pdftotext` on each input file to generate `.txt` files
- Converts text files to CSV format with basic parsing
- `--help` option with detailed usage and examples
- `--version` option showing version 1.0.0
- `--merge OUTPUT_FILE` option to combine multiple CSVs into one file

**Project Organization:**
- `pdf2csv.py`: Main executable script (755 permissions)
- `doc/`: Documentation directory with prompts.md and structure.md
- `examples/`: Usage examples and practical documentation
- `tests/`: Test suite with basic functionality verification
- `requirements.txt`: Python dependencies (minimal, uses standard library)

**Code Structure:**
- Object-oriented design with `PDF2CSVConverter` class
- Proper error handling and user feedback
- System dependency checking (pdftotext availability)
- Clean separation of concerns: PDF→text→CSV conversion pipeline

**Testing & Validation:**
- Created test suite that verifies help/version options and error handling
- All basic tests pass successfully
- Script is immediately usable with real PDF files

The implementation follows vibe coding principles with clean, intuitive code that can be iteratively improved based on actual bank statement formats encountered.

---

### 2025-09-03 - Session 3
#### Prompt:
I want to keep trace of our whole conversation. Every entry into prompt.md should containt the prompt and your answer.

#### AI Response:
I updated the `doc/prompts.md` file to include complete traceability by adding both user prompts and AI responses for each interaction. The format now includes:

**Enhanced Documentation Structure:**
- Clear session numbering and dates
- Both user prompts and detailed AI responses
- Complete conversation history for analysis
- Better organization for future reference

**Updated Format:**
- Each entry now has "Prompt:" and "AI Response:" sections
- Detailed summaries of what was implemented
- Technical details about code structure and features
- Testing and validation results

This comprehensive documentation supports the vibe coding experimental approach by providing complete context for how the project evolved through AI-assisted development, allowing for better analysis of the development process and decision-making patterns.

---

### 2025-09-03 - Session 4
#### Prompt:
Create a parser object able to read a text file from pdftotext. Put it into a separate directory. Connect the script to the parser. The parset object will receive the text filename as parmater for the constructor. It needs method to extract informations read in the file, like bank name, banque identification, start_date, end_date as well than a collection of bank statements. The bank statements should be an object too. update prompts.md with this prompt.

#### AI Response:
I created a comprehensive parser system with proper object-oriented architecture:

**New Directory Structure:**
- `src/`: Main source directory
- `src/models.py`: Data models for BankStatement and BankTransaction objects
- `src/parsers/`: Parser package directory
- `src/parsers/base_parser.py`: Abstract base parser and GenericTextParser
- `src/parsers/specific_parsers.py`: FrenchBankParser for French bank statements
- `tests/test_parsers.py`: Comprehensive parser testing suite

**Data Models Created:**
- `BankTransaction` dataclass: Represents individual transactions with date, description, amount, balance, reference, category
- `BankStatement` dataclass: Contains bank metadata (name, code, account info, date ranges) and transaction collection
- Both models include CSV conversion methods and string representations

**Parser Architecture:**
- `BaseStatementParser` (abstract): Defines interface for all parsers
- `GenericTextParser`: Handles common bank statement patterns using regex
- `FrenchBankParser`: Specialized for French banking formats with Euro currency and French date/amount patterns

**Key Parser Features:**
- Constructor takes text filename parameter as requested
- Methods to extract: bank_name, bank_identification, start_date, end_date, transactions collection
- Automatic text file loading and parsing
- Regex-based pattern matching for dates, amounts, bank names
- Error handling and fallback processing

**Integration with Main Script:**
- Updated `pdf2csv.py` to use the new parser system
- Enhanced CSV output with structured data from parsers
- Fallback to basic text processing if parser fails
- Improved merge functionality using proper CSV handling

**Testing & Validation:**
- Created comprehensive test suite that validates all parser functionality
- Tests show successful extraction of bank info, dates, and transactions
- All parser tests pass: Generic parser, French parser, and CSV output
- Example extractions: "CRÉDIT AGRICOLE", account numbers, date ranges, transaction parsing

The system follows vibe coding principles with clean abstractions that can be easily extended for different bank formats while maintaining robust fallback mechanisms.