import os
import yaml
from cli import BudgetCLI
from transactions_manager import TransactionsManager

TRANSACTIONS_FILE_NAME = "transactions.csv"
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
            with open(file_path, 'w') as f:
                yaml.dump(default_content, f, default_flow_style=False)

def main():
    # Ensure configuration files exist before starting
    ensure_config_files_exist()

    manager = TransactionsManager(
        TRANSACTIONS_FILE_NAME,
        NEW_TRANSACTIONS_FILE,
        CONFIG_FILE,
        CATEGORIES_FILE,
        MAPPINGS_FILE
    )
    cli = BudgetCLI(manager)
    cli.run()

if __name__ == "__main__":
    main()
