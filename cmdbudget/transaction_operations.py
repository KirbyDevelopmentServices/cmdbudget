# AI generated and maintained by claude-3.7-sonnet
# This file provides a unified API for transaction CRUD operations
# License: MIT

import os
import csv
import logging # Import logging
from datetime import datetime
from typing import Dict, List, Optional
from .transaction import Transaction, RawTransaction
from .utils import parse_date_multi_format # Import from utils

# Get a logger for this module
logger = logging.getLogger(__name__)

# Define standard CSV fieldnames once
CSV_FIELDNAMES = [
    "Transaction Date", "Description", "Amount", "Currency",
    "Category", "Subcategory", "Tag", "Merchant"
]

class TransactionOperations:
    """Provides a unified API for transaction CRUD operations against a CSV file."""

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
        # Basic validation can be added here if desired
        if not isinstance(date, datetime):
             # Handle cases where date might not be datetime object yet
             # This shouldn't happen if called correctly, but defensive check
             logger.warning(f"create_transaction received non-datetime object for date: {type(date)}")
             # Attempt to parse if it looks like a string? Or raise error?
             # For now, let it proceed, but Transaction init might fail
             pass
        return Transaction(
            _date=date,
            _description=description,
            _amount=float(amount), # Ensure amount is float
            currency=currency,
            category=category,
            subcategory=subcategory,
            tag=tag,
            merchant=merchant
        )

    @staticmethod
    def save_transaction(transaction: Transaction, file_path: str) -> bool:
        """Save a transaction to the specified file. Returns True on success, False otherwise."""
        try:
            transaction_row = TransactionOperations._transaction_to_row(transaction)
            return TransactionOperations._append_transaction_to_file(transaction_row, file_path)
        except Exception as e:
            logger.error(f"Error during save_transaction for '{transaction.description}': {e}", exc_info=True)
            return False

    @staticmethod
    def _transaction_to_row(transaction: Transaction) -> Dict[str, str]: # Make private
        """Convert a Transaction object to a row dictionary for CSV storage."""
        # Use the specified dd/mm/yy format for writing
        date_format = "%d/%m/%y"
        return {
            "Transaction Date": transaction.date.strftime(date_format),
            "Description": transaction.description,
            # Store amount with 2 decimal places consistently (positive=expense)
            "Amount": f"{transaction.amount:.2f}",
            "Currency": transaction.currency,
            "Category": transaction.category,
            "Subcategory": transaction.subcategory,
            "Tag": transaction.tag,
            "Merchant": transaction.merchant
        }

    @staticmethod
    def _append_transaction_to_file(transaction_row: Dict[str, str], file_path: str) -> bool: # Make private
        """Append a transaction row to a CSV file."""
        try:
            # Check if file exists and is empty to write header
            file_exists = os.path.exists(file_path)
            write_header = not file_exists or os.path.getsize(file_path) == 0

            with open(file_path, 'a', newline='', encoding='utf-8') as file: # Specify encoding
                writer = csv.DictWriter(file, fieldnames=CSV_FIELDNAMES)

                if write_header:
                    writer.writeheader()

                writer.writerow(transaction_row)
            return True
        except IOError as e:
            logger.error(f"I/O Error appending transaction to {file_path}: {e}", exc_info=True)
            return False
        except Exception as e:
            logger.error(f"Unexpected error appending transaction to {file_path}: {e}", exc_info=True)
            return False

    @staticmethod
    def read_transactions(file_path: str) -> List[Transaction]:
        """Read all transactions from a CSV file. Returns list of Transactions or empty list on error."""
        transactions = []
        try:
            if not os.path.exists(file_path):
                logger.info(f"Transaction file {file_path} not found, returning empty list.")
                return []

            with open(file_path, 'r', encoding='utf-8') as file: # Specify encoding
                reader = csv.DictReader(file)
                # Check header consistency
                if set(reader.fieldnames) != set(CSV_FIELDNAMES):
                     logger.warning(f"CSV header mismatch in {file_path}. Expected: {CSV_FIELDNAMES}, Found: {reader.fieldnames}")
                     # Attempt to proceed, but Transaction.from_row might fail if columns missing.

                # Define a specific parser for the known stored date format
                def parse_stored_date(date_str):
                    try:
                        return datetime.strptime(date_str, "%d/%m/%y")
                    except ValueError as e:
                        # Re-raise with more context if specific format fails
                        raise ValueError(f"Error parsing stored date '{date_str}' with format %d/%m/%y: {e}") from e

                line_num = 1 # For error reporting (header is line 1)
                for row in reader:
                    line_num += 1
                    try:
                        # Ensure all required keys are present before parsing
                        if not all(key in row for key in CSV_FIELDNAMES):
                             logger.error(f"Missing one or more required columns in row {line_num} of {file_path}. Skipping row: {row}")
                             continue
                        # Parse the transaction first, using the specific stored date parser
                        parsed_transaction = Transaction.from_row(row, parse_stored_date)
                        # Log details *before* appending
                        logger.info(f"LOADED TX (L{line_num}): Date={parsed_transaction.date.date()}, Desc='{parsed_transaction.description}', Amount={parsed_transaction.amount}, Category='{parsed_transaction.category}'")
                        transactions.append(parsed_transaction)
                    except ValueError as e:
                        logger.error(f"Error parsing transaction from row {line_num} in {file_path}: {e} - Row: {row}")
                    except Exception as e:
                         logger.error(f"Unexpected error processing row {line_num} in {file_path}: {e} - Row: {row}", exc_info=True)

            return transactions
        except IOError as e:
            logger.error(f"I/O Error reading transactions from {file_path}: {e}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Unexpected error reading transactions from {file_path}: {e}", exc_info=True)
            return []

    # Removed parse_date_multi_format - moved to utils.py
    # Removed check_transaction_exists - responsibility lies higher up

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
    
    # @staticmethod
    # def check_transaction_exists(transaction: Transaction, existing_transactions: List[Transaction]) -> bool:
    #     """Check if a transaction already exists in the list."""
    #     return transaction in existing_transactions 