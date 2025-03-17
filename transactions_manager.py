import csv
from datetime import datetime
from collections import defaultdict
from typing import List, Dict, Tuple
from transaction import Transaction
from transaction_processor import NewTransactionProcessor
from transaction_reporter import TransactionReporter
import yaml

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
        return datetime.strptime(date_str, "%m/%d/%y")

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