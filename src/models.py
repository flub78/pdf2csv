"""
Data models for bank statement parsing.

This module contains the data structures used to represent
bank statements and transactions.
"""

from datetime import datetime
from typing import Optional, List
from dataclasses import dataclass


@dataclass
class BankTransaction:
    """Represents a single bank transaction."""
    
    date: Optional[datetime] = None
    value_date: Optional[datetime] = None
    description: str = ""
    operation_type: str = ""
    amount: Optional[float] = None
    debit: Optional[float] = None
    credit: Optional[float] = None
    balance: Optional[float] = None
    reference: str = ""
    category: str = ""
    libelle_interbancaire: str = ""  # For special transaction categories like "PAIEMENT CB"
    
    def __str__(self) -> str:
        date_str = self.date.strftime("%Y-%m-%d") if self.date else "N/A"
        return f"{date_str}: {self.description} - {self.amount} (Balance: {self.balance})"
    
    def to_csv_row(self) -> List[str]:
        """Convert transaction to CSV row format."""
        date_str = self.date.strftime("%Y-%m-%d") if self.date else ""
        amount_str = str(self.amount) if self.amount is not None else ""
        balance_str = str(self.balance) if self.balance is not None else ""
        
        return [
            date_str,
            self.description,
            amount_str,
            balance_str,
            self.reference,
            self.category
        ]
    
    @classmethod
    def csv_header(cls) -> List[str]:
        """Return CSV header for transactions."""
        return ["Date", "Description", "Amount", "Balance", "Reference", "Category"]


@dataclass
class BankStatement:
    """Represents a complete bank statement with metadata and transactions."""
    
    bank_name: str = ""
    bank_code: str = ""  # Bank identification code
    account_number: str = ""
    account_holder: str = ""
    client_name: str = ""
    client_section: str = ""  # Client section (e.g., "SECTION VOL MOTEUR")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    opening_balance: Optional[float] = None
    closing_balance: Optional[float] = None
    final_balance: Optional[float] = None
    transactions: List[BankTransaction] = None
    
    def __post_init__(self):
        if self.transactions is None:
            self.transactions = []
    
    def add_transaction(self, transaction: BankTransaction):
        """Add a transaction to the statement."""
        self.transactions.append(transaction)
    
    def get_transaction_count(self) -> int:
        """Get the number of transactions."""
        return len(self.transactions)
    
    def get_date_range_str(self) -> str:
        """Get formatted date range string."""
        if self.start_date and self.end_date:
            start_str = self.start_date.strftime("%Y-%m-%d")
            end_str = self.end_date.strftime("%Y-%m-%d")
            return f"{start_str} to {end_str}"
        return "Date range not available"
    
    def to_csv_data(self) -> List[List[str]]:
        """Convert statement to CSV data format."""
        data = []
        
        # Add header
        data.append(BankTransaction.csv_header())
        
        # Add transactions
        for transaction in self.transactions:
            data.append(transaction.to_csv_row())
        
        return data
    
    def __str__(self) -> str:
        return (f"Bank Statement - {self.bank_name}\n"
                f"Account: {self.account_number}\n"
                f"Period: {self.get_date_range_str()}\n"
                f"Transactions: {self.get_transaction_count()}")
