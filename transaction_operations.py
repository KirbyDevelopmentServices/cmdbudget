# AI generated and maintained by claude-3.7-sonnet
# This file provides a unified API for transaction CRUD operations
# License: MIT

import os
import csv
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from transaction import Transaction, RawTransaction

class TransactionOperations:
    """Provides a unified API for transaction CRUD operations."""
    
    @staticmethod
    def create_transaction(
        date: datetime,
        description: str,
        amount: float,
        currency: str,
        category: str,
        subcategory: str = "",
        tag: str = "",
        merchant: str = ""
    ) -> Transaction:
        """Create a new Transaction object with the given attributes."""
        return Transaction(
            _date=date,
            _description=description,
            _amount=float(amount),
            currency=currency,
            category=category,
            subcategory=subcategory,
            tag=tag,
            merchant=merchant
        )
    
    @staticmethod
    def save_transaction(transaction: Transaction, file_path: str) -> bool:
        """Save a transaction to the specified file."""
        transaction_row = TransactionOperations.transaction_to_row(transaction)
        return TransactionOperations.append_transaction_to_file(transaction_row, file_path)
    
    @staticmethod
    def transaction_to_row(transaction: Transaction) -> Dict[str, str]:
        """Convert a Transaction object to a row dictionary for CSV storage."""
        return {
            "Transaction Date": transaction.date.strftime("%m/%d/%y"),
            "Description": transaction.description,
            "Amount": str(transaction.amount),
            "Currency": transaction.currency,
            "Category": transaction.category,
            "Subcategory": transaction.subcategory,
            "Tag": transaction.tag,
            "Merchant": transaction.merchant
        }
    
    @staticmethod
    def append_transaction_to_file(transaction_row: Dict[str, str], file_path: str) -> bool:
        """Append a transaction row to a CSV file."""
        try:
            file_exists = os.path.exists(file_path)
            
            with open(file_path, 'a', newline='') as file:
                fieldnames = [
                    "Transaction Date", "Description", "Amount", "Currency",
                    "Category", "Subcategory", "Tag", "Merchant"
                ]
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                
                if not file_exists:
                    writer.writeheader()
                    
                writer.writerow(transaction_row)
            return True
        except Exception as e:
            print(f"Error saving transaction: {e}")
            return False
    
    @staticmethod
    def read_transactions(file_path: str, date_parser) -> List[Transaction]:
        """Read all transactions from a CSV file."""
        transactions = []
        try:
            if not os.path.exists(file_path):
                return []
                
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(Transaction.from_row(row, date_parser))
            return transactions
        except Exception as e:
            print(f"Error reading transactions: {e}")
            return []
    
    @staticmethod
    def parse_date_multi_format(date_str: str) -> datetime:
        """Parse date string in multiple formats."""
        formats = [
            "%m/%d/%y",     # 01/15/23
            "%m/%d/%Y",     # 01/15/2023
            "%Y-%m-%d",     # 2023-01-15
            "%d/%m/%y",     # 15/01/23
            "%d/%m/%Y"      # 15/01/2023
        ]
        
        for date_format in formats:
            try:
                return datetime.strptime(date_str, date_format)
            except ValueError:
                continue
                
        raise ValueError(f"Unable to parse date: {date_str}")
    
    @staticmethod
    def check_transaction_exists(transaction: Transaction, existing_transactions: List[Transaction]) -> bool:
        """Check if a transaction already exists in the list."""
        return transaction in existing_transactions 