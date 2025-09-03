#!/usr/bin/env python3
"""
pdf2csv - Convert PDF bank statements to CSV files

This script extracts text from PDF files using pdftotext and converts
them to CSV format using structured parsers. It supports processing 
multiple files and can merge them into a single output file.

Author: Created with AI assistance
License: MIT
"""

import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

# Add src directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

try:
    from parsers import GenericTextParser
    from models import BankStatement
except ImportError as e:
    print(f"Error importing parser modules: {e}")
    print("Make sure the src/ directory structure is correct")
    sys.exit(1)


__version__ = "1.0.0"


class PDF2CSVConverter:
    """Main converter class for PDF to CSV conversion."""
    
    def __init__(self, merge_output: Optional[str] = None):
        """
        Initialize the converter.
        
        Args:
            merge_output: If provided, all files will be merged into this single CSV file
        """
        self.merge_output = merge_output
        self.processed_files = []
        
    def check_pdftotext_available(self) -> bool:
        """Check if pdftotext is available in the system."""
        try:
            result = subprocess.run(['pdftotext', '-v'], 
                                  capture_output=True, 
                                  text=True, 
                                  check=False)
            return result.returncode == 0 or 'pdftotext' in result.stderr.lower()
        except FileNotFoundError:
            return False
    
    def convert_pdf_to_text(self, pdf_path: Path) -> Optional[Path]:
        """
        Convert a PDF file to text using pdftotext.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Path to the generated text file, or None if conversion failed
        """
        if not pdf_path.exists():
            print(f"Error: File {pdf_path} does not exist")
            return None
            
        # Generate output text file path
        txt_path = pdf_path.with_suffix('.txt')
        
        try:
            # Run pdftotext command
            cmd = ['pdftotext', str(pdf_path), str(txt_path)]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            if txt_path.exists():
                print(f"Successfully converted: {pdf_path} -> {txt_path}")
                return txt_path
            else:
                print(f"Error: Text file was not created for {pdf_path}")
                return None
                
        except subprocess.CalledProcessError as e:
            print(f"Error converting {pdf_path}: {e}")
            if e.stderr:
                print(f"Error details: {e.stderr}")
            return None
        except Exception as e:
            print(f"Unexpected error converting {pdf_path}: {e}")
            return None
    
    def process_text_to_csv(self, txt_path: Path) -> Optional[Path]:
        """
        Process text file and convert to CSV format using structured parser.
        
        Args:
            txt_path: Path to the text file
            
        Returns:
            Path to the generated CSV file, or None if conversion failed
        """
        if not txt_path.exists():
            print(f"Error: Text file {txt_path} does not exist")
            return None
        
        csv_path = txt_path.with_suffix('.csv')
        
        try:
            # Use the parser to extract structured data
            parser = GenericTextParser(str(txt_path))
            statement = parser.parse()
            
            # Display extracted information
            print(f"  Bank: {statement.bank_name}")
            print(f"  Account: {statement.account_number}")
            print(f"  Period: {statement.get_date_range_str()}")
            print(f"  Transactions: {statement.get_transaction_count()}")
            
            # Write to CSV using the structured data
            with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                
                # Get CSV data from statement
                csv_data = statement.to_csv_data()
                writer.writerows(csv_data)
            
            print(f"Successfully created CSV: {csv_path}")
            return csv_path
            
        except Exception as e:
            print(f"Error processing {txt_path} to CSV: {e}")
            # Fallback to basic text processing
            return self._fallback_text_to_csv(txt_path)
    
    def _fallback_text_to_csv(self, txt_path: Path) -> Optional[Path]:
        """
        Fallback method for basic text to CSV conversion.
        
        Args:
            txt_path: Path to the text file
            
        Returns:
            Path to the generated CSV file, or None if conversion failed
        """
        csv_path = txt_path.with_suffix('.csv')
        
        try:
            with open(txt_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
            
            with open(csv_path, 'w', encoding='utf-8') as csv_file:
                # Write CSV header
                csv_file.write("Date,Description,Amount,Balance\n")
                
                # Basic conversion - write raw text
                lines = content.strip().split('\n')
                for line in lines:
                    if line.strip():
                        # Escape quotes and commas for CSV
                        escaped_line = line.replace('"', '""')
                        csv_file.write(f',,"{escaped_line}",\n')
            
            print(f"Created basic CSV (fallback): {csv_path}")
            return csv_path
            
        except Exception as e:
            print(f"Error in fallback processing {txt_path}: {e}")
            return None
    
    def merge_csv_files(self, csv_files: List[Path], output_path: Path) -> bool:
        """
        Merge multiple CSV files into a single file.
        
        Args:
            csv_files: List of CSV file paths to merge
            output_path: Path for the merged output file
            
        Returns:
            True if successful, False otherwise
        """
        if not csv_files:
            print("No CSV files to merge")
            return False
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as merged_file:
                writer = csv.writer(merged_file)
                header_written = False
                
                for csv_file in csv_files:
                    if not csv_file.exists():
                        print(f"Warning: CSV file {csv_file} does not exist, skipping")
                        continue
                    
                    with open(csv_file, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        
                        for i, row in enumerate(reader):
                            # Write header only once
                            if i == 0:  # Header line
                                if not header_written:
                                    writer.writerow(row)
                                    header_written = True
                            else:  # Data lines
                                writer.writerow(row)
            
            print(f"Successfully merged {len(csv_files)} files into {output_path}")
            return True
            
        except Exception as e:
            print(f"Error merging CSV files: {e}")
            return False
    
    def process_files(self, pdf_files: List[str]) -> bool:
        """
        Process a list of PDF files.
        
        Args:
            pdf_files: List of PDF file paths
            
        Returns:
            True if all files were processed successfully, False otherwise
        """
        if not self.check_pdftotext_available():
            print("Error: pdftotext is not available. Please install poppler-utils:")
            print("  Ubuntu/Debian: sudo apt-get install poppler-utils")
            print("  CentOS/RHEL/Fedora: sudo yum install poppler-utils")
            return False
        
        csv_files = []
        success_count = 0
        
        for pdf_file in pdf_files:
            pdf_path = Path(pdf_file).resolve()
            print(f"\nProcessing: {pdf_path}")
            
            # Convert PDF to text
            txt_path = self.convert_pdf_to_text(pdf_path)
            if txt_path is None:
                continue
            
            # Convert text to CSV
            csv_path = self.process_text_to_csv(txt_path)
            if csv_path is None:
                continue
            
            csv_files.append(csv_path)
            success_count += 1
        
        # Handle merge option
        if self.merge_output and csv_files:
            merge_path = Path(self.merge_output).resolve()
            if self.merge_csv_files(csv_files, merge_path):
                print(f"\nMerged output saved to: {merge_path}")
        
        print(f"\nProcessing complete. Successfully processed {success_count}/{len(pdf_files)} files.")
        return success_count == len(pdf_files)


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert PDF bank statements to CSV files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s statement1.pdf statement2.pdf
  %(prog)s --merge combined.csv *.pdf
  %(prog)s --help
  %(prog)s --version
        """
    )
    
    parser.add_argument(
        'files',
        nargs='*',
        help='PDF files to convert'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '--merge',
        metavar='OUTPUT_FILE',
        help='Merge all converted files into a single CSV file'
    )
    
    args = parser.parse_args()
    
    # Check if files were provided
    if not args.files:
        parser.print_help()
        print("\nError: No PDF files specified")
        return 1
    
    # Create converter instance
    converter = PDF2CSVConverter(merge_output=args.merge)
    
    # Process files
    success = converter.process_files(args.files)
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
