import csv
import os
import yaml
import logging
from typing import Set, List
from datetime import datetime
from transaction import Transaction, RawTransaction
from pprint import pprint, pformat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TransactionClassifier:
    def __init__(self, config_file, categories_file, mappings_file):
        self.config_file = config_file
        self.categories_file = categories_file
        self.mappings_file = mappings_file
        self.config = self.load_yaml(config_file)
        categories_data = self.load_yaml(categories_file)['categories']
        # Store categories and their subcategories
        self.categories = list(categories_data.keys())
        self.subcategories = categories_data
        self.mappings = self.load_yaml(mappings_file)['mappings']

    @staticmethod
    def load_yaml(file_path):
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Warning: {file_path} not found. Creating empty file.")
            default_content = {'mappings': {}} if 'mappings' in file_path else {}
            with open(file_path, 'w') as file:
                yaml.dump(default_content, file)
            return default_content

    def save_mapping(self, description: str, category: str, subcategory: str = None):
        """Save new mapping to the mappings file."""
        self.mappings[description] = {
            'category': category,
            'subcategory': subcategory
        }
        with open(self.mappings_file, 'w') as file:
            yaml.dump({'mappings': self.mappings}, file)

    def find_category(self, description: str) -> tuple[str, str]:
        """Find category and subcategory for a description or return None, None."""
        for known_desc, mapping in self.mappings.items():
            if known_desc.upper() in description.upper():
                return mapping['category'], mapping.get('subcategory')
        return None, None

    def prompt_for_category(self, description: str) -> tuple[str, str]:
        """Prompt user to select a category and subcategory."""
        print(f"\nTransaction: {description}")
        
        while True:
            print("\nSelect a category:")
            # Filter out IGNORED and SPLIT from display categories
            display_categories = [cat for cat in self.categories if cat not in ["IGNORED", "SPLIT"]]
            
            # Display existing categories
            for i, category in enumerate(display_categories, 1):
                print(f"{i}. {category}")
            print(f"{len(display_categories) + 1}. Add new category")
            
            try:
                choice = int(input("\nEnter category number: "))
                if 1 <= choice <= len(display_categories):
                    selected_category = display_categories[choice - 1]
                    return self._handle_subcategory_selection(selected_category)
                elif choice == len(display_categories) + 1:
                    # Handle new category creation
                    new_category = input("Enter new category name: ").strip()
                    if not new_category:
                        print("Category name cannot be empty. Please try again.")
                        continue
                    
                    if new_category in self.categories:
                        print("Category already exists. Please try again.")
                        continue
                    
                    # Add new category to categories
                    self.categories.append(new_category)
                    self.subcategories[new_category] = []
                    
                    # Save updated categories to file
                    with open(self.categories_file, 'w') as file:
                        yaml.dump({'categories': self.subcategories}, file)
                    
                    print(f"Added new category: {new_category}")
                    return self._handle_subcategory_selection(new_category)
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def _handle_subcategory_selection(self, category: str) -> tuple[str, str]:
        """Handle subcategory selection for a given category."""
        while True:
            subcategories = self.subcategories[category]
            if not subcategories:
                add_subcategory = input("\nNo subcategories exist. Would you like to add one? (y/n): ").lower()
                if add_subcategory != 'y':
                    return category, ""
            else:
                print(f"\nSelect a subcategory for {category}:")
                print("0. [No Subcategory]")
                for i, subcat in enumerate(subcategories, 1):
                    print(f"{i}. {subcat}")
                print(f"{len(subcategories) + 1}. Add new subcategory")
            
            try:
                subchoice = int(input("\nEnter subcategory number: "))
                if subchoice == 0:
                    return category, ""
                elif 1 <= subchoice <= len(subcategories):
                    return category, subcategories[subchoice - 1]
                elif subchoice == len(subcategories) + 1:
                    # Handle new subcategory creation
                    new_subcategory = input("Enter new subcategory name: ").strip()
                    if not new_subcategory:
                        print("Subcategory name cannot be empty. Please try again.")
                        continue
                    
                    if new_subcategory in subcategories:
                        print("Subcategory already exists. Please try again.")
                        continue
                    
                    # Add new subcategory
                    self.subcategories[category].append(new_subcategory)
                    
                    # Save updated categories to file
                    with open(self.categories_file, 'w') as file:
                        yaml.dump({'categories': self.subcategories}, file)
                    
                    print(f"Added new subcategory: {new_subcategory}")
                    return category, new_subcategory
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")


class NewTransactionProcessor:
    def __init__(self, new_transactions_file, transactions_file, config_file, categories_file, mappings_file):
        self.new_transactions_file = new_transactions_file
        self.transactions_file = transactions_file
        self.classifier = TransactionClassifier(config_file, categories_file, mappings_file)
        self.existing_transactions: Set[Transaction] = set()

    def load_existing_transactions(self) -> Set[Transaction]:
        """Load and hash all existing transactions."""
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                return {Transaction.from_row(row, self.parse_date) for row in reader}
        except FileNotFoundError:
            logger.info(f"No existing transactions file found at {self.transactions_file}")
            return set()

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        # Try multiple date formats
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

    def process(self) -> bool:
        """Process transactions from new_transactions.csv"""
        if not os.path.exists(self.new_transactions_file):
            logger.info("No new transactions file found.")
            return False

        self.existing_transactions = self.load_existing_transactions()
        processed_count = 0

        try:
            with open(self.new_transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                config = self.classifier.config['csv_structure']
                
                for row in reader:
                    logger.debug("Processing transaction:\n%s", pformat(row))
                    try:
                        # Add debug logging
                        logger.debug(f"Processing date: {row[config['date_column']]}")
                        
                        # Take absolute value of amount before creating RawTransaction
                        amount_field = config['amount_column']
                        if amount_field in row:
                            try:
                                # Store the exact amount from the row
                                exact_amount = abs(float(row[amount_field]))
                                row[amount_field] = str(exact_amount)
                            except ValueError as e:
                                logger.error(f"Error converting amount '{row[amount_field]}' to number: {e}")
                                continue
                        
                        # Create a RawTransaction for comparison
                        raw_transaction = RawTransaction.from_row(row, config, self.parse_date)
                    except ValueError as e:
                        logger.error(f"Date parsing error: {e} for row: {row}")
                        continue

                    # Check if transaction already exists
                    if raw_transaction in self.existing_transactions:
                        logger.info(f"Skipping duplicate transaction: {raw_transaction.description} "
                                  f"on {raw_transaction.date} for {raw_transaction.amount}")
                        continue

                    # Check for existing mapping first
                    category, subcategory = self.classifier.find_category(raw_transaction.description)
                    if category:
                        # We have a mapping, process automatically
                        transaction = Transaction.from_raw(
                            raw_transaction,
                            config['default_currency'],
                            category,
                            subcategory
                        )
                        
                        transaction_row = {
                            "Transaction Date": transaction.date.strftime("%m/%d/%y"),
                            "Description": transaction.description,
                            "Amount": str(transaction.amount),
                            "Currency": transaction.currency,
                            "Category": transaction.category,
                            "Subcategory": transaction.subcategory,
                            "Tag": transaction.tag,
                            "Merchant": transaction.merchant
                        }

                        self._append_transaction_to_file(transaction_row)
                        processed_count += 1
                        logger.info(f"Added transaction: {transaction.description}")
                        continue

                    # No mapping exists, present options to user
                    while True:
                        print(f"\nNew Transaction: {raw_transaction.description}")
                        print(f"Amount: ${exact_amount:.2f}")
                        print("1. Show full details")
                        print("2. Categorize")
                        print("3. Split transaction")
                        print("4. Ignore")
                        
                        try:
                            choice = int(input("\nSelect an option (1-4): "))
                            if choice == 1:
                                self._display_transaction_details(row, config)
                                continue
                            elif choice == 2:
                                category, subcategory = self._process_categorization(raw_transaction)
                                break
                            elif choice == 3:
                                self._handle_split_transaction(raw_transaction, exact_amount)
                                # Skip the transaction creation since splits are already written
                                processed_count += 1
                                continue  # Continue to next transaction in the main loop
                            elif choice == 4:
                                category, subcategory = "IGNORED", ""
                                break
                            else:
                                print("Invalid choice. Please try again.")
                        except ValueError as e:
                            if "invalid literal for int()" in str(e):
                                print("Please enter a valid number.")
                            else:
                                logger.error(f"Error processing choice: {e}")
                                print("An error occurred. Skipping this transaction.")
                                continue

                    # Only create and write transaction if we didn't split
                    if choice != 3:
                        # Create full transaction
                        transaction = Transaction.from_raw(
                            raw_transaction,
                            config['default_currency'],
                            category,
                            subcategory
                        )
                        
                        # Convert to row for CSV
                        transaction_row = {
                            "Transaction Date": transaction.date.strftime("%m/%d/%y"),
                            "Description": transaction.description,
                            "Amount": str(transaction.amount),
                            "Currency": transaction.currency,
                            "Category": transaction.category,
                            "Subcategory": transaction.subcategory,
                            "Tag": transaction.tag,
                            "Merchant": transaction.merchant
                        }

                        # Immediately write the transaction to the file
                        self._append_transaction_to_file(transaction_row)
                        processed_count += 1
                        logger.info(f"Added transaction: {transaction.description}")

            logger.info(f"Processed {processed_count} new transactions.")
            return processed_count > 0

        except Exception as e:
            logger.error(f"Error processing new transactions: {e}")
            return False

    def _display_transaction_details(self, row: dict, config: dict):
        """Display all transaction details in a user-friendly format."""
        print("\n=== Transaction Details ===")
        
        # Filter out empty/None values
        cleaned_row = {
            field: value for field, value in row.items() 
            if value and value != "" and field != "None"
        }
        
        # Pretty print the transaction details
        pprint(cleaned_row, indent=2)
        print("========================\n")

    def _handle_split_transaction(self, raw_transaction: RawTransaction, exact_amount: float):
        """Handle splitting a transaction into multiple parts."""
        # Prepare the original SPLIT transaction
        split_transactions = [{
            "Transaction Date": raw_transaction.date.strftime("%m/%d/%y"),
            "Description": raw_transaction.description,
            "Amount": str(exact_amount),
            "Currency": self.classifier.config['csv_structure']['default_currency'],
            "Category": "SPLIT",
            "Subcategory": "",
            "Tag": "",
            "Merchant": ""
        }]
        
        remaining_amount = exact_amount
        
        while remaining_amount > 0:
            print(f"\nRemaining amount to split: ${remaining_amount:.2f}")
            split_choice = input("Would you like to add another split? (y/n): ").lower()
            
            if split_choice != 'y':
                if remaining_amount > 0:
                    print(f"Warning: ${remaining_amount:.2f} of the transaction will be unaccounted for.")
                break
            
            while True:
                try:
                    split_amount = float(input("Enter split amount: $"))
                    if split_amount <= 0:
                        print("Amount must be positive.")
                    elif split_amount > remaining_amount:
                        print(f"Amount cannot exceed remaining amount (${remaining_amount:.2f})")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")
            
            split_description = input("Enter description for this split: ")
            
            # Get category and subcategory for the split
            category, subcategory = self.classifier.prompt_for_category(split_description)
            
            # Add the split transaction to our list
            split_transactions.append({
                "Transaction Date": raw_transaction.date.strftime("%m/%d/%y"),
                "Description": split_description,
                "Amount": str(split_amount),
                "Currency": self.classifier.config['csv_structure']['default_currency'],
                "Category": category,
                "Subcategory": subcategory,
                "Tag": "",
                "Merchant": ""
            })
            
            remaining_amount -= split_amount
        
        # Write all transactions at once
        for transaction in split_transactions:
            self._append_transaction_to_file(transaction)

    def _process_categorization(self, raw_transaction: RawTransaction) -> tuple[str, str]:
        """Handle the categorization process for a transaction."""
        # Normal categorization process for unsplit transactions
        category, subcategory = self.classifier.find_category(raw_transaction.description)
        
        if not category:
            category, subcategory = self.classifier.prompt_for_category(raw_transaction.description)
            if category not in ["IGNORED", "SPLIT"]:
                save_mapping = input("Save this mapping for future transactions? (y/n): ").lower()
                if save_mapping == 'y':
                    self.classifier.save_mapping(raw_transaction.description, category, subcategory)
        
        return category, subcategory

    def _append_transaction_to_file(self, transaction_row: dict):
        """Append a single transaction to the transactions file."""
        file_exists = os.path.exists(self.transactions_file)
        
        with open(self.transactions_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(transaction_row.keys()))
            if not file_exists:
                writer.writeheader()
            writer.writerow(transaction_row) 