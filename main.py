# AI generated and maintained by Gemini 2.5 Pro
# This file handles the initialization and main application flow
# License: MIT

import os
import yaml
from cli import BudgetCLI
from transactions_manager import TransactionsManager

# Remove the hardcoded constant
# TRANSACTIONS_FILE_NAME = "transactions.csv"
NEW_TRANSACTIONS_FILE = "new_transactions.csv"
CONFIG_FILE = "config.yml"
CATEGORIES_FILE = "categories.yml"
MAPPINGS_FILE = "transaction_mappings.yml"

def ensure_config_files_exist():
    """Ensure all necessary configuration files exist with default values."""
    
    # Default configurations
    default_config = {
        'csv_structure': {
            'description_column': 'Description',
            'amount_column': 'Amount',
            'date_column': 'Transaction Date',
            'default_currency': 'CAD'
        },
        # Add default storage configuration
        'storage': {
            'transaction_file_path': 'transactions.csv'
        }
    }

    default_categories = {
        'categories': {
            'IGNORED': [],
            'SPLIT': [],
            'Groceries': [],
            'Entertainment': [],
            'Transportation': [],
            'Housing': [],
            'Utilities': [],
            'Healthcare': [],
            'Personal': [],
            'Misc': []
        }
    }

    default_mappings = {
        'mappings': {}
    }

    # Dictionary of files and their default contents
    config_files = {
        CONFIG_FILE: default_config,
        CATEGORIES_FILE: default_categories,
        MAPPINGS_FILE: default_mappings
    }

    for file_path, default_content in config_files.items():
        if not os.path.exists(file_path):
            print(f"Creating default {file_path}...")
            try:
                with open(file_path, 'w') as f:
                    yaml.dump(default_content, f, default_flow_style=False)
            except IOError as e:
                print(f"Error creating default file {file_path}: {e}")
                # Exit or handle error appropriately if config creation fails
                exit(1)

def load_config(file_path):
    """Load configuration from a YAML file."""
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file {file_path} not found.")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file {file_path}: {e}")
        return None
    except IOError as e:
        print(f"Error reading configuration file {file_path}: {e}")
        return None

def main():
    # Ensure configuration files exist before starting
    ensure_config_files_exist()

    # Load configuration
    config = load_config(CONFIG_FILE)
    if not config:
        print("Exiting due to configuration load failure.")
        return

    # Determine the transaction file path from config, using default if necessary
    transactions_file_path = config.get('storage', {}).get('transaction_file_path', 'transactions.csv')
    # Ensure the directory for the transaction file exists
    transactions_dir = os.path.dirname(transactions_file_path)
    if transactions_dir and not os.path.exists(transactions_dir):
        try:
            os.makedirs(transactions_dir)
            print(f"Created directory for transactions: {transactions_dir}")
        except OSError as e:
            print(f"Error creating directory {transactions_dir}: {e}")
            return # Exit if we can't create the necessary directory

    manager = TransactionsManager(
        transactions_file_path, # Pass the configured path
        NEW_TRANSACTIONS_FILE,
        CONFIG_FILE,
        CATEGORIES_FILE,
        MAPPINGS_FILE
    )
    cli = BudgetCLI(manager)
    cli.run()

if __name__ == "__main__":
    main()
