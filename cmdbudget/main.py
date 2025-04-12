# AI generated and maintained by claude-3.7-sonnet
# This file is the main entry point for the cmdbudget application
# License: MIT

import sys
import os
import yaml
import logging # Import logging
import csv # Added for creating default transactions file
from .cli import BudgetCLI
from .transactions_manager import TransactionsManager
from .display import Display # Import Display

# --- Configuration Setup --- 
CONFIG_FILE = 'config.yml'
CATEGORIES_FILE = 'categories.yml'
MAPPINGS_FILE = 'transaction_mappings.yml'
DEFAULT_TRANSACTIONS_FILE = 'transactions.csv'
DEFAULT_NEW_TRANSACTIONS_FILE = 'new_transactions.csv'

# --- Basic Logging Configuration --- 
# Configure logging level and format
# Consider adding file logging later
# Remove console handler setup
# logging.basicConfig(
#     level=logging.INFO, 
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )

# Keep logger instance for potential internal logging (e.g., to file later)
logger = logging.getLogger(__name__)

def load_config():
    """Loads configuration from YAML file, creates default storage config, and validates structure."""
    default_storage_config = {
        'transaction_file_path': DEFAULT_TRANSACTIONS_FILE,
        'new_transaction_file_path': DEFAULT_NEW_TRANSACTIONS_FILE
    }
    # Remove default_csv_structure dictionary

    if not os.path.exists(CONFIG_FILE):
        Display.warning(f"{CONFIG_FILE} not found. Creating default configuration with storage paths only.")
        # Only create default storage config
        default_config = {
            'storage': default_storage_config 
        }
        try:
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(default_config, file)
            Display.message(f"Default {CONFIG_FILE} created with default storage settings.")
            Display.error(f"Please edit {CONFIG_FILE} to add the required 'import_csv_structure' section before running again.")
            sys.exit(f"Configuration incomplete. Exiting.")
        except IOError as e:
            Display.error(f"Could not create default {CONFIG_FILE}: {e}")
            sys.exit(f"Error: Could not create {CONFIG_FILE}. Exiting.")

    # Load existing config file
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file: 
            config = yaml.safe_load(file)
            if not config: 
                 Display.error(f"{CONFIG_FILE} is empty. Please provide a valid configuration.")
                 sys.exit(f"Error: {CONFIG_FILE} is empty. Exiting.")

            # --- Validation and Defaulting --- 
            # 1. Validate REQUIRED 'import_csv_structure' section
            if 'import_csv_structure' not in config:
                Display.error(f"Required section 'import_csv_structure' not found in {CONFIG_FILE}.")
                sys.exit(f"Configuration error: Missing 'import_csv_structure' section. Exiting.")
            
            csv_config = config['import_csv_structure'] # Use the new name

            if not isinstance(csv_config, dict):
                Display.error(f"'import_csv_structure' section in {CONFIG_FILE} must be a dictionary.")
                sys.exit(f"Error: Invalid 'import_csv_structure' section. Exiting.")
            
            # Check for required keys within import_csv_structure
            required_csv_keys = ['date_column', 'description_column', 'amount_column']
            for key in required_csv_keys:
                if key not in csv_config:
                    Display.error(f"Missing required key '{key}' in {CONFIG_FILE}['import_csv_structure'].")
                    sys.exit(f"Error: Invalid CSV structure configuration. Exiting.")
            
            # Handle OPTIONAL keys within import_csv_structure, providing defaults
            if 'default_currency' not in csv_config:
                 Display.warning(f"'default_currency' missing in {CONFIG_FILE}['import_csv_structure']. Using default: 'CAD'")
                 csv_config['default_currency'] = 'CAD'
            if 'expenses_are_positive' not in csv_config:
                 Display.warning(f"'expenses_are_positive' missing in {CONFIG_FILE}['import_csv_structure']. Using default: True")
                 csv_config['expenses_are_positive'] = True
            # Validate the type of expenses_are_positive
            if not isinstance(csv_config.get('expenses_are_positive'), bool):
                 Display.error(f"'expenses_are_positive' in {CONFIG_FILE}['import_csv_structure'] must be true or false.")
                 sys.exit(f"Error: Invalid value for 'expenses_are_positive'. Exiting.")

            # 2. Handle optional 'storage' section
            if 'storage' not in config:
                Display.warning(f"'storage' section not found in {CONFIG_FILE}. Using default file paths: {default_storage_config}")
                config['storage'] = default_storage_config
            else:
                 # Validate storage structure if present
                 if not isinstance(config['storage'], dict):
                      Display.error(f"'storage' section in {CONFIG_FILE} must be a dictionary.")
                      sys.exit(f"Error: Invalid 'storage' section. Exiting.")
                 # Apply defaults for missing keys within storage
                 if 'transaction_file_path' not in config['storage']:
                      Display.warning(f"'transaction_file_path' missing in {CONFIG_FILE}['storage']. Using default: {DEFAULT_TRANSACTIONS_FILE}")
                      config['storage']['transaction_file_path'] = DEFAULT_TRANSACTIONS_FILE
                 if 'new_transaction_file_path' not in config['storage']:
                      Display.warning(f"'new_transaction_file_path' missing in {CONFIG_FILE}['storage']. Using default: {DEFAULT_NEW_TRANSACTIONS_FILE}")
                      config['storage']['new_transaction_file_path'] = DEFAULT_NEW_TRANSACTIONS_FILE

            logger.debug(f"Loaded configuration: {config}")
            return config
    except yaml.YAMLError as e:
        # Use Display.error instead of logger.error
        Display.error(f"Error parsing {CONFIG_FILE}: {e}")
        sys.exit(f"Error: Could not parse {CONFIG_FILE}. Exiting.")
    except IOError as e:
        # Use Display.error instead of logger.error
        Display.error(f"Could not read {CONFIG_FILE}: {e}")
        sys.exit(f"Error: Could not read {CONFIG_FILE}. Exiting.")
    except Exception as e:
        # Keep internal error log call
        logger.error(f"Unexpected error loading {CONFIG_FILE}: {e}", exc_info=True)
        # Use Display.error for user feedback
        Display.error(f"Unexpected error loading {CONFIG_FILE}. Please check logs.")
        sys.exit(f"Error loading {CONFIG_FILE}. Exiting.")

def create_default_yaml(file_path, default_content):
     """Creates a default YAML file if it doesn't exist."""
     if not os.path.exists(file_path):
         # Use Display.warning instead of logger.warning
         Display.warning(f"{file_path} not found. Creating default file.")
         try:
             with open(file_path, 'w', encoding='utf-8') as file:
                 yaml.dump(default_content, file)
             # Use Display.message instead of logger.info
             Display.message(f"Default {file_path} created.")
         except IOError as e:
             # Use Display.error instead of logger.error
             Display.error(f"Could not create default {file_path}: {e}")
             # Optionally exit if this file is critical
             # sys.exit(f"Error creating {file_path}. Exiting.")

def main():
    """Main application entry point."""
    # Use Display.message instead of logger.info for startup message
    # (Commented out for now, perhaps not needed for user)
    
    # Load configuration (handles defaults for storage and csv_structure)
    config = load_config()
    
    # Ensure other YAML files exist, creating defaults if necessary
    create_default_yaml(CATEGORIES_FILE, {'categories': {"IGNORED": [], "SPLIT": []}})
    create_default_yaml(MAPPINGS_FILE, {'mappings': {}})
    
    # Get file paths from config (load_config guarantees these keys exist)
    try:
        transactions_file = config['storage']['transaction_file_path']
        new_transactions_file = config['storage']['new_transaction_file_path']
    except KeyError as e:
         # This should ideally not happen due to load_config handling defaults
         logger.critical(f"Critical error retrieving guaranteed storage path '{e}'. This indicates a bug in load_config.")
         sys.exit("Internal configuration error. Exiting.")
    
    # Check if the main transactions file exists, create if not
    if not os.path.exists(transactions_file):
         # Use Display.warning instead of logger.warning
         Display.warning(f"Main transaction file '{transactions_file}' not found. Creating empty file with headers.")
         try:
             # Use TransactionOperations field names for consistency
             from .transaction_operations import CSV_FIELDNAMES 
             with open(transactions_file, 'w', newline='', encoding='utf-8') as f:
                 writer = csv.writer(f)
                 writer.writerow(CSV_FIELDNAMES) 
             # Use Display.message instead of logger.info
             Display.message(f"Created empty transaction file: {transactions_file}")
         except IOError as e:
             # Use Display.error instead of logger.error
             Display.error(f"Could not create transaction file '{transactions_file}': {e}")
             sys.exit(f"Error creating {transactions_file}. Exiting.")
         except ImportError:
             # Use Display.error instead of logger.error
             Display.error("Could not import CSV_FIELDNAMES from transaction_operations. Cannot create transaction file header.")
             sys.exit("Initialization error. Exiting.")
         except Exception as e: # Catch other potential errors during file creation
             # Keep internal log call
             logger.error(f"Unexpected error creating transaction file '{transactions_file}': {e}", exc_info=True)
             # Use Display.error for user
             Display.error(f"Unexpected error creating transaction file '{transactions_file}'. Check logs.")
             sys.exit(f"Error creating {transactions_file}. Exiting.")

    # Initialize manager and CLI
    try:
        manager = TransactionsManager(
            transactions_file=transactions_file,
            new_transactions_file=new_transactions_file,
            config_file=CONFIG_FILE,
            categories_file=CATEGORIES_FILE,
            mappings_file=MAPPINGS_FILE
        )
        cli = BudgetCLI(manager)
        cli.run()
    except Exception as e:
         # Keep internal critical log call
         logger.critical(f"Fatal error during application initialization or run: {e}", exc_info=True)
         # Use Display.error for user
         Display.error(f"A critical error occurred: {e}\nPlease check the application logs for more details.")
         sys.exit(1) # Exit with a non-zero code

if __name__ == "__main__":
    main()
