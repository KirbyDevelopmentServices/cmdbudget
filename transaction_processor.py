# AI generated and maintained by claude-3.7-sonnet
# This file handles processing and categorizing new transactions
# License: MIT

import csv
import os
import yaml
import logging
from typing import Set, List
from datetime import datetime
from transaction import Transaction, RawTransaction
from transaction_operations import TransactionOperations
from pprint import pprint, pformat
from utils import parse_date_multi_format # Import from utils

logging.basicConfig(level=logging.INFO) # Basic config, might be moved to main
logger = logging.getLogger(__name__)

class TransactionClassifier:
    def __init__(self, config_file, categories_file, mappings_file):
        self.config_file = config_file
        self.categories_file = categories_file
        self.mappings_file = mappings_file
        self.config = self.load_yaml(config_file)
        categories_data = self.load_yaml(categories_file).get('categories', {})
        self.categories = list(categories_data.keys())
        self.subcategories = categories_data
        self.mappings = self.load_yaml(mappings_file).get('mappings', {})

    @staticmethod
    def load_yaml(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file: # Specify encoding
                return yaml.safe_load(file) or {}
        except FileNotFoundError:
            logger.warning(f"YAML file {file_path} not found. Creating default.") # Use logger
            default_content = {}
            if 'mappings' in file_path:
                default_content = {'mappings': {}}
            elif 'categories' in file_path:
                 # Default should include protected categories
                 default_content = {'categories': {"IGNORED": [], "SPLIT": []}} 
            elif 'config' in file_path:
                 # Define default config structure if needed
                 default_content = {
                     'csv_structure': {
                         'date_column': 'Transaction Date', # Example defaults
                         'description_column': 'Description', 
                         'amount_column': 'Amount',
                         'default_currency': 'CAD' 
                     }, 
                     'storage': {
                         'transaction_file_path': 'transactions.csv'
                     }
                 }
            
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    yaml.dump(default_content, file)
                logger.info(f"Created default YAML file: {file_path}")
            except IOError as e:
                 logger.error(f"Failed to create default YAML file {file_path}: {e}", exc_info=True)
                 # Depending on severity, might want to raise an exception or exit
            return default_content
        except yaml.YAMLError as e:
             logger.error(f"Error parsing YAML file {file_path}: {e}", exc_info=True)
             return {} # Return empty dict on parsing error
        except Exception as e:
            logger.error(f"Unexpected error loading YAML file {file_path}: {e}", exc_info=True)
            return {}

    def save_mapping(self, description: str, category: str, subcategory: str = None):
        """Save new mapping to the mappings file."""
        self.mappings[description] = {
            'category': category,
            'subcategory': subcategory
        }
        try:
            with open(self.mappings_file, 'w', encoding='utf-8') as file:
                yaml.dump({'mappings': self.mappings}, file)
            logger.info(f"Saved new mapping for '{description[:30]}...'")
        except IOError as e:
             logger.error(f"Failed to save mappings file {self.mappings_file}: {e}", exc_info=True)
        except Exception as e:
             logger.error(f"Unexpected error saving mappings file {self.mappings_file}: {e}", exc_info=True)

    def find_category(self, description: str) -> tuple[str, str]:
        """Find category and subcategory for a description or return None, None."""
        # Consider making matching case-insensitive by default
        # Consider more robust matching (e.g., partial, regex)
        for known_desc, mapping in self.mappings.items():
            if known_desc.upper() in description.upper(): # Case-insensitive check
                return mapping['category'], mapping.get('subcategory')
        return None, None

    def prompt_for_category(self, description: str) -> tuple[str, str]:
        """Prompt user to select a category and subcategory."""
        # This function primarily uses print for user interaction, which is correct
        # Keep print statements here
        print(f"\nTransaction: {description}")

        while True:
            print("\nSelect a category:")
            display_categories = [cat for cat in self.categories if cat not in ["IGNORED", "SPLIT"]]
            display_categories.sort() # Sort for consistency

            for i, category in enumerate(display_categories, 1):
                print(f"{i}. {category}")
            print(f"{len(display_categories) + 1}. Add new category")

            try:
                choice_input = input("\nEnter category number: ")
                if not choice_input: continue # Handle empty input
                choice = int(choice_input)

                if 1 <= choice <= len(display_categories):
                    selected_category = display_categories[choice - 1]
                    # Pass description for context in subcategory handling if needed
                    return self._handle_subcategory_selection(selected_category, description)
                elif choice == len(display_categories) + 1:
                    new_category = input("Enter new category name: ").strip()
                    if not new_category:
                        print("Category name cannot be empty.")
                        continue
                    if new_category in self.categories:
                        print("Category already exists.")
                        continue
                    if new_category in ["IGNORED", "SPLIT"]:
                         print("Cannot create category with reserved name.")
                         continue

                    # Add new category and save
                    self.categories.append(new_category)
                    self.subcategories[new_category] = []
                    if self._save_categories():
                        print(f"Added new category: {new_category}")
                        return self._handle_subcategory_selection(new_category, description)
                    else:
                         # Failed to save, remove from in-memory lists
                         self.categories.remove(new_category)
                         del self.subcategories[new_category]
                         print("Error saving new category. Please try again.")
                         continue # Go back to category selection
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    def _handle_subcategory_selection(self, category: str, description: str) -> tuple[str, str]:
        """Handle subcategory selection for a given category."""
        # Keep print statements here for user interaction
        while True:
            subcategories = self.subcategories.get(category, [])
            subcategories.sort() # Sort for consistency

            print(f"\nSelect a subcategory for {category} (Transaction: {description[:50]}...):")
            print("0. [No Subcategory]")
            if not subcategories:
                print("(No existing subcategories)")
            else:
                for i, subcat in enumerate(subcategories, 1):
                    print(f"{i}. {subcat}")
            print(f"{len(subcategories) + 1}. Add new subcategory")

            try:
                subchoice_input = input("\nEnter subcategory number: ")
                if not subchoice_input: continue
                subchoice = int(subchoice_input)

                if subchoice == 0:
                    return category, ""
                elif 1 <= subchoice <= len(subcategories):
                    return category, subcategories[subchoice - 1]
                elif subchoice == len(subcategories) + 1:
                    new_subcategory = input("Enter new subcategory name: ").strip()
                    if not new_subcategory:
                        print("Subcategory name cannot be empty.")
                        continue
                    if new_subcategory in subcategories:
                        print("Subcategory already exists.")
                        continue

                    # Add new subcategory and save
                    if category not in self.subcategories:
                        self.subcategories[category] = []
                    self.subcategories[category].append(new_subcategory)

                    if self._save_categories():
                        print(f"Added new subcategory: {new_subcategory}")
                        return category, new_subcategory
                    else:
                         # Failed to save, remove from in-memory list
                         self.subcategories[category].remove(new_subcategory)
                         print("Error saving new subcategory. Please try again.")
                         continue # Go back to subcategory selection
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")

    def _save_categories(self) -> bool:
         """Saves the current categories and subcategories to the YAML file."""
         try:
             with open(self.categories_file, 'w', encoding='utf-8') as file:
                 yaml.dump({'categories': self.subcategories}, file)
             logger.info(f"Categories saved to {self.categories_file}")
             return True
         except IOError as e:
             logger.error(f"Failed to save categories file {self.categories_file}: {e}", exc_info=True)
             return False
         except Exception as e:
             logger.error(f"Unexpected error saving categories file {self.categories_file}: {e}", exc_info=True)
             return False


class NewTransactionProcessor:
    def __init__(self, new_transactions_file, transactions_file, config_file, categories_file, mappings_file):
        self.new_transactions_file = new_transactions_file
        self.transactions_file = transactions_file
        self.classifier = TransactionClassifier(config_file, categories_file, mappings_file)
        self.existing_transactions: Set[Transaction] = set()
        self.transaction_ops = TransactionOperations()

    def load_existing_transactions(self) -> Set[Transaction]:
        """Load and hash all existing transactions from the main transaction file."""
        # Use the read_transactions method from TransactionOperations
        transactions = self.transaction_ops.read_transactions(self.transactions_file)
        # Ensure they are hashable (depends on Transaction.__hash__ implementation)
        return set(transactions)

    # Removed parse_date static method - use imported utility

    def process(self) -> bool:
        """Process transactions from new_transactions.csv"""
        if not os.path.exists(self.new_transactions_file):
            logger.info("No new transactions file found.")
            return False

        self.existing_transactions = self.load_existing_transactions()
        processed_count = 0
        config = self.classifier.config.get('csv_structure', {})
        if not config:
            logger.error("CSV structure configuration not found in config.yml")
            return False
        default_currency = config.get('default_currency', 'CAD')

        try:
            # Ensure consistent encoding
            with open(self.new_transactions_file, 'r', encoding='utf-8-sig') as file: # Use utf-8-sig for potential BOM
                reader = csv.DictReader(file)
                line_num = 1 # For error reporting
                for row in reader:
                    line_num += 1
                    logger.debug(f"Processing row {line_num}: {pformat(row)}")
                    raw_transaction = None # Initialize

                    try:
                        # Use the RawTransaction.from_row factory method
                        # It requires the row, config, and the date parser
                        raw_transaction = RawTransaction.from_row(row, config, parse_date_multi_format)

                    # Catch parsing/creation errors for this specific row
                    except ValueError as e: # Catches date/amount parsing errors within from_row
                        logger.error(f"Data parsing error in row {line_num}: {e}. Skipping row: {row}")
                        continue
                    except KeyError as e:
                        logger.error(f"Missing expected column '{e}' in row {line_num} based on config. Skipping row: {row}")
                        continue
                    except Exception as e:
                         logger.error(f"Unexpected error processing data in row {line_num}: {e}. Skipping row: {row}", exc_info=True)
                         continue

                    # --- Duplicate Check --- 
                    if raw_transaction in self.existing_transactions:
                        logger.info(f"Skipping duplicate transaction from row {line_num}: {raw_transaction.description}")
                        continue

                    # --- Categorization --- 
                    category, subcategory = self.classifier.find_category(raw_transaction.description)
                    if category:
                        # Mapping found - save automatically
                        transaction = Transaction.from_raw(raw_transaction, default_currency, category, subcategory)
                        if self.transaction_ops.save_transaction(transaction, self.transactions_file):
                            processed_count += 1
                            logger.info(f"Added transaction via mapping (Row {line_num}): {transaction.description}")
                            self.existing_transactions.add(transaction)
                        else:
                             logger.error(f"Failed to save mapped transaction (Row {line_num}): {transaction.description}")
                        continue # Move to the next row

                    # --- User Interaction for Unmapped Transactions --- 
                    choice = None
                    # Get amount for display before loop (assuming from_row succeeded)
                    exact_amount = raw_transaction.amount
                    while choice is None:
                         # Print statements for user interaction are kept here
                         print(f"\nNew Transaction (Row {line_num}): {raw_transaction.description}")
                         print(f"Amount: ${exact_amount:.2f} {default_currency}")

                         print("1. Show full details")
                         print("2. Categorize")
                         print("3. Split transaction")
                         print("4. Ignore")
                         choice_input = input("\nSelect an option (1-4): ").strip()
                         # ... (rest of the user interaction loop remains largely the same, using print)
                         if not choice_input: choice = None; continue
                         try:
                              choice = int(choice_input)
                              if choice == 1:
                                   # Pass the original row data stored by from_row if available,
                                   # otherwise, just print the known details.
                                   details_to_show = getattr(raw_transaction, '_raw_data', None) or \
                                                     {'Date': raw_transaction.date, 'Description': raw_transaction.description, 'Amount': raw_transaction.amount}
                                   self._display_transaction_details(details_to_show, config)
                                   choice = None # Loop back
                              elif choice == 2:
                                   category, subcategory = self._process_categorization(raw_transaction)
                                   break # Proceed to save
                              elif choice == 3:
                                   # Pass amount directly from raw_transaction
                                   self._handle_split_transaction(raw_transaction, raw_transaction.amount, default_currency)
                                   # Add split marker to prevent re-processing if import runs again on same file
                                   split_marker = Transaction.from_raw(raw_transaction, default_currency, "SPLIT", None)
                                   self.existing_transactions.add(split_marker)
                                   processed_count += 1 # Count the original as processed via split
                                   break # Break from inner loop, skip standard save
                              elif choice == 4:
                                   category, subcategory = "IGNORED", ""
                                   break # Proceed to save as IGNORED
                              else:
                                   print("Invalid choice.")
                                   choice = None # Loop back
                         except ValueError:
                              print("Please enter a valid number.")
                              choice = None # Loop back
                         except Exception as e:
                              logger.error(f"Error processing user choice for row {line_num}: {e}", exc_info=True)
                              print("An error occurred during processing. Skipping this transaction.")
                              # Decide: skip row (break) or try again (choice=None)? Let's skip.
                              break # Break from inner loop, will skip saving

                    # --- Save Transaction (if not split or error) --- 
                    if choice in [2, 4]:
                        transaction = Transaction.from_raw(raw_transaction, default_currency, category, subcategory)
                        if self.transaction_ops.save_transaction(transaction, self.transactions_file):
                            processed_count += 1
                            log_action = "Ignored" if category == "IGNORED" else "Added"
                            logger.info(f"{log_action} transaction (Row {line_num}): {transaction.description}")
                            self.existing_transactions.add(transaction)
                        else:
                            logger.error(f"Failed to save transaction (Row {line_num}): {transaction.description}")

                    # Reset choice for next iteration if needed, although break/continue handles flow
                    choice = None 
            
            logger.info(f"Finished processing. {processed_count} new transactions added.")
            # Consider moving/archiving the new_transactions.csv file here
            # e.g., os.rename(self.new_transactions_file, f"{self.new_transactions_file}.processed_{datetime.now().strftime('%Y%m%d%H%M%S')}")
            return processed_count > 0

        except FileNotFoundError:
             logger.error(f"File not found during processing: {self.new_transactions_file}")
             return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during CSV processing loop: {e}", exc_info=True)
            return False

    def _display_transaction_details(self, details: dict, config: dict):
        """Display transaction details. Keeps print for direct output."""
        print("\n=== Transaction Details ===")
        # Use the provided details dictionary
        cleaned_row = {
            field: value for field, value in details.items()
            if value and value != "" and field != "None"
        }
        pprint(cleaned_row, indent=2)
        print("========================\n")


    def _handle_split_transaction(self, raw_transaction: RawTransaction, exact_amount: float, default_currency: str):
        """Handle splitting a transaction. Uses print for user interaction."""
        # ... (Create and save SPLIT marker transaction - already uses logging)
        split_marker_transaction = self.transaction_ops.create_transaction(
            date=raw_transaction.date,
            description=raw_transaction.description,
            amount=exact_amount,
            currency=default_currency,
            category="SPLIT", subcategory="", tag="", merchant=""
        )
        if not self.transaction_ops.save_transaction(split_marker_transaction, self.transactions_file):
             logger.error(f"Failed to save SPLIT marker for: {raw_transaction.description}. Aborting split.")
             print("Error saving initial split record. Cannot proceed with splitting.")
             return # Abort splitting
        else:
             logger.info(f"Marked original transaction as SPLIT: {raw_transaction.description}")
             self.existing_transactions.add(split_marker_transaction)

        remaining_amount = exact_amount
        splits_added = 0

        while remaining_amount > 0.009:
            # Print statements for user interaction are kept
            print(f"\nRemaining amount to split: ${remaining_amount:.2f} {default_currency}")
            split_choice = input("Add another split? (y/n): ").lower().strip()
            if split_choice != 'y':
                if remaining_amount > 0.009:
                    print(f"Warning: ${remaining_amount:.2f} will remain categorized as SPLIT.")
                break
            
            split_amount = None
            while split_amount is None:
                 # ... (Input logic for split_amount using print)
                 try:
                    split_amount_input = input("Enter split amount: $").strip()
                    if not split_amount_input: continue
                    split_amount_val = float(split_amount_input)

                    if split_amount_val <= 0.009:
                        print("Amount must be positive.")
                    elif split_amount_val > remaining_amount + 0.001:
                        print(f"Amount cannot exceed remaining amount (${remaining_amount:.2f})")
                    else:
                         split_amount = split_amount_val # Assign valid amount
                 except ValueError:
                    print("Please enter a valid number.")

            split_description = input(f"Enter description for this ${split_amount:.2f} split [Split: {raw_transaction.description[:30]}...]: ").strip()
            if not split_description:
                split_description = f"Split: {raw_transaction.description}"

            category, subcategory = self.classifier.prompt_for_category(split_description)

            new_split_transaction = self.transaction_ops.create_transaction(
                date=raw_transaction.date,
                description=split_description,
                amount=split_amount,
                currency=default_currency,
                category=category, subcategory=subcategory, tag="", merchant=""
            )

            if self.transaction_ops.save_transaction(new_split_transaction, self.transactions_file):
                logger.info(f"Added split part: {split_description} ${split_amount:.2f}")
                self.existing_transactions.add(new_split_transaction)
                remaining_amount -= split_amount
                splits_added += 1
            else:
                 logger.error(f"Failed to save split transaction part: {split_description}. Stopping split.")
                 print("Error saving split part. Aborting further splits for this transaction.")
                 break
        
        if splits_added > 0:
             logger.info(f"Finished splitting transaction '{raw_transaction.description}' into {splits_added} parts.")
        elif remaining_amount < 0.009: # Successfully allocated everything
             logger.info(f"Finished splitting transaction '{raw_transaction.description}'. Full amount allocated.")


    def _process_categorization(self, raw_transaction: RawTransaction) -> tuple[str, str]:
        """Handle categorization. Uses print for user interaction."""
        category, subcategory = self.classifier.find_category(raw_transaction.description)
        if not category:
            category, subcategory = self.classifier.prompt_for_category(raw_transaction.description)
            if category not in ["IGNORED", "SPLIT"]:
                # Keep print for user confirmation
                save_mapping = input("Save this mapping for future transactions? (y/n): ").lower().strip()
                if save_mapping == 'y':
                    self.classifier.save_mapping(raw_transaction.description, category, subcategory)
        return category, subcategory

# Removed redundant _append_transaction_to_file method

# Remove the redundant _append_transaction_to_file method
#    def _append_transaction_to_file(self, transaction_row: dict):
#        """Append a single transaction to the transactions file."""
#        return self.transaction_ops.append_transaction_to_file(transaction_row, self.transactions_file) 