# AI generated and maintained by claude-3.7-sonnet
# This file manages transaction data operations
# License: MIT

import csv
import os
from datetime import datetime, date
from collections import defaultdict
from typing import List, Dict, Tuple
from transaction import Transaction
from transaction_processor import NewTransactionProcessor, TransactionClassifier
from transaction_reporter import TransactionReporter
from transaction_operations import TransactionOperations
import yaml
from transactions_editor import TransactionEditor

class TransactionsManager:
    """Manages transaction data and operations."""
    
    def __init__(self, transactions_file, new_transactions_file, config_file, categories_file, mappings_file):
        self.transactions_file = transactions_file
        self.new_transactions_file = new_transactions_file
        self.config_file = config_file
        self.categories_file = categories_file
        self.mappings_file = mappings_file
        self.data = self.load_csv()
        self.transactions = None
        self.month_grouped_transactions = None
        self.reporter = None
        self.classifier = TransactionClassifier(config_file, categories_file, mappings_file)
        self.editor = TransactionEditor(transactions_file, self.classifier)
        self.transaction_ops = TransactionOperations()

    def load_csv(self) -> List[Dict]:
        """Reads the CSV file and returns its contents as a list of dictionaries."""
        try:
            with open(self.transactions_file, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                return list(reader)
        except FileNotFoundError:
            print(f"Error: The file '{self.transactions_file}' was not found.")
        except Exception as e:
            print(f"Error reading file '{self.transactions_file}': {e}")

    def initialize_data(self):
        """Load and organize all transaction data upfront."""
        self.transactions = self.build_transactions()
        # Include IGNORED transactions in storage but not in reporting
        self.month_grouped_transactions = self.group_by_month(self.transactions)
        self.reporter = TransactionReporter(self.transactions, self.month_grouped_transactions)

    def build_transactions(self) -> List[Transaction]:
        """Build Transaction objects from CSV data."""
        return [Transaction.from_row(row, self.parse_date) for row in self.data]

    def group_by_month(self, transactions: List[Transaction]) -> Dict[Tuple[int, int], List[Transaction]]:
        """Group transactions by month."""
        monthly_transaction_groups = defaultdict(list)
        for transaction in transactions:
            year_month_tuple = (transaction.date.year, transaction.date.month)
            monthly_transaction_groups[year_month_tuple].append(transaction)
        return monthly_transaction_groups

    def get_transactions_for_month(self, month_key: Tuple[int, int]) -> List[Transaction]:
        """Get all transactions for a specific month."""
        return self.month_grouped_transactions[month_key]

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        """Parse a date string using multiple formats."""
        return TransactionOperations.parse_date_multi_format(date_str)

    def process_new_transactions(self):
        """Process transactions from new_transactions.csv"""
        processor = NewTransactionProcessor(
            self.new_transactions_file,
            self.transactions_file,
            self.config_file,
            self.categories_file,
            self.mappings_file
        )
        if processor.process():
            # Reinitialize data to include new transactions
            self.initialize_data() 

    def get_categories(self) -> set:
        """Get all available categories."""
        with open(self.categories_file, 'r') as file:
            categories = yaml.safe_load(file)
            # Filter out IGNORED from displayed categories
            return {cat for cat in categories.get('categories', []) if cat != "IGNORED"}

    def add_category(self, category: str) -> bool:
        """Add a new category. Returns True if successful, False if category already exists."""
        if category == "IGNORED":
            return False  # Prevent adding IGNORED as a user category
        
        categories = self.get_categories()
        if category in categories:
            return False
        
        categories.add(category)
        with open(self.categories_file, 'w') as file:
            # Make sure to preserve IGNORED in the file even if we don't show it
            all_categories = sorted(list(categories) + ["IGNORED"])
            yaml.dump({'categories': all_categories}, file)
        return True

    def delete_category(self, category: str) -> bool:
        """Delete a category. Returns True if successful."""
        categories = self.get_categories()
        if category in categories:
            categories.remove(category)
            with open(self.categories_file, 'w') as file:
                yaml.dump({'categories': sorted(list(categories))}, file)
            return True
        return False

    def has_transactions_with_category(self, category: str) -> bool:
        """Check if any transactions use this category."""
        return any(t.category == category for t in self.transactions) 

    def edit_transaction(self, transaction: Transaction) -> bool:
        """Edit an existing transaction."""
        result = self.editor.edit_transaction(transaction)
        if result:
            # Reinitialize data to include edited transactions
            self.initialize_data()
        return result 

    def add_custom_transaction(self):
        """Add a custom transaction manually entered by the user."""
        print("\n=== Add Custom Transaction ===")
        
        # Get transaction date (default to today)
        while True:
            date_str = input("Transaction Date (dd/mm/yyyy) [today]: ").strip()
            if not date_str:
                # Default to today
                transaction_date = date.today()
                break
            try:
                transaction_date = datetime.strptime(date_str, "%d/%m/%Y").date()
                break
            except ValueError:
                print("Invalid date format. Please use dd/mm/yyyy format.")
        
        # Get description
        while True:
            description = input("Description: ").strip()
            if description:
                break
            print("Description cannot be empty.")
        
        # Get amount
        while True:
            amount_str = input("Amount: $").strip()
            try:
                amount = float(amount_str)
                if amount <= 0:
                    print("Amount must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid amount. Please enter a valid number.")
        
        # Get currency (default to CAD)
        while True:
            print("\nSelect currency:")
            print("1. CAD")
            print("2. USD")
            currency_choice = input("Select currency [1]: ").strip()
            if not currency_choice:
                currency = "CAD"
                break
            try:
                choice = int(currency_choice)
                if choice == 1:
                    currency = "CAD"
                    break
                elif choice == 2:
                    currency = "USD"
                    break
                else:
                    print("Invalid choice. Please select 1 or 2.")
            except ValueError:
                print("Invalid choice. Please select 1 or 2.")
        
        # Check if there's an existing mapping for this description
        category, subcategory = self.classifier.find_category(description)
        
        if category:
            print(f"\nFound existing mapping for this description:")
            print(f"Category: {category}")
            print(f"Subcategory: {subcategory if subcategory else 'None'}")
            use_mapping = input("Use this mapping? (y/n): ").lower().strip()
            
            if use_mapping != 'y':
                # User doesn't want to use existing mapping, prompt for new categorization
                category, subcategory = self.classifier.prompt_for_category(description)
        else:
            # No mapping found, prompt for categorization
            category, subcategory = self.classifier.prompt_for_category(description)
        
        # Create the transaction using our new operations class
        transaction = self.transaction_ops.create_transaction(
            date=transaction_date,
            description=description,
            amount=amount,
            currency=currency,
            category=category,
            subcategory=subcategory,
            tag="",
            merchant=""
        )
        
        # Save the transaction to CSV
        self.transaction_ops.save_transaction(transaction, self.transactions_file)
        print(f"\nTransaction added successfully: {description} (${amount:.2f} {currency})")
        
        # Reinitialize data to include the new transaction
        self.initialize_data()
        return True
    
    def _append_transaction_to_file(self, transaction):
        """Append a transaction to the transactions file."""
        return self.transaction_ops.save_transaction(transaction, self.transactions_file) 