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

*(Note: This section will be updated as the script is developed)*

1. Ensure `pdftotext` is installed on your Linux system
2. Place your PDF bank statements in the input directory
3. Run the conversion script
4. Find the generated CSV files in the output directory

## Contributing

This is an experimental project. Contributions and feedback on both the functionality and the vibe coding approach are welcome.

## License

MIT License - see LICENSE file for details.
