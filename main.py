# AI generated and maintained by claude-3.7-sonnet
# This file is the main entry point for the cmdbudget application
# License: MIT

import sys
import os
import yaml
import logging # Import logging
import csv # Added for creating default transactions file
from cli import BudgetCLI
from transactions_manager import TransactionsManager

# --- Configuration Setup --- 
CONFIG_FILE = 'config.yml'
CATEGORIES_FILE = 'categories.yml'
MAPPINGS_FILE = 'transaction_mappings.yml'
DEFAULT_TRANSACTIONS_FILE = 'transactions.csv'
DEFAULT_NEW_TRANSACTIONS_FILE = 'new_transactions.csv'

# --- Basic Logging Configuration --- 
# Configure logging level and format
# Consider adding file logging later
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_config():
    """Loads configuration from YAML file, creates defaults, and validates structure."""
    default_storage_config = {
        'transaction_file_path': DEFAULT_TRANSACTIONS_FILE,
        'new_transaction_file_path': DEFAULT_NEW_TRANSACTIONS_FILE
    }
    default_csv_structure = {
        'date_column': 'Transaction Date',
        'description_column': 'Description',
        'amount_column': 'Amount',
        'default_currency': 'CAD',
        'expenses_are_positive': True # Default: expenses in CSV are positive numbers
    }

    if not os.path.exists(CONFIG_FILE):
        logger.warning(f"{CONFIG_FILE} not found. Creating default configuration.")
        default_config = {
            'csv_structure': default_csv_structure, # Use default structure
            'storage': default_storage_config # Include default storage here
        }
        try:
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(default_config, file)
            logger.info(f"Default {CONFIG_FILE} created.")
            return default_config
        except IOError as e:
            logger.error(f"Could not create default {CONFIG_FILE}: {e}")
            sys.exit(f"Error: Could not create {CONFIG_FILE}. Exiting.")

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file: # Specify encoding
            config = yaml.safe_load(file)
            if not config: # Handle empty file
                 logger.error(f"{CONFIG_FILE} is empty. Please provide a valid configuration.")
                 sys.exit(f"Error: {CONFIG_FILE} is empty. Exiting.")

            # --- Validation and Defaulting --- 
            # 1. Handle optional/defaulting 'csv_structure'
            if 'csv_structure' not in config:
                logger.warning(f"'csv_structure' section not found in {CONFIG_FILE}. Using defaults.")
                config['csv_structure'] = default_csv_structure
            else:
                # Ensure it's a dictionary
                if not isinstance(config['csv_structure'], dict):
                    logger.error(f"'csv_structure' section in {CONFIG_FILE} must be a dictionary.")
                    sys.exit(f"Error: Invalid 'csv_structure' section in {CONFIG_FILE}. Exiting.")
                # Check for required keys within csv_structure
                required_csv_keys = ['date_column', 'description_column', 'amount_column']
                for key in required_csv_keys:
                    if key not in config['csv_structure']:
                        logger.error(f"Missing required key '{key}' in {CONFIG_FILE}['csv_structure'].")
                        sys.exit(f"Error: Invalid CSV structure in {CONFIG_FILE}. Exiting.")
                # Add defaults for optional keys if missing
                if 'default_currency' not in config['csv_structure']:
                     logger.warning(f"'default_currency' missing in {CONFIG_FILE}['csv_structure']. Using default: 'CAD'")
                     config['csv_structure']['default_currency'] = 'CAD' # Example default
                if 'expenses_are_positive' not in config['csv_structure']:
                     logger.warning(f"'expenses_are_positive' missing in {CONFIG_FILE}['csv_structure']. Using default: True")
                     config['csv_structure']['expenses_are_positive'] = True
                 # Validate the type of expenses_are_positive
                if not isinstance(config['csv_structure'].get('expenses_are_positive'), bool):
                     logger.error(f"'expenses_are_positive' in {CONFIG_FILE}['csv_structure'] must be true or false.")
                     sys.exit(f"Error: Invalid value for 'expenses_are_positive' in {CONFIG_FILE}. Exiting.")

            # 2. Handle optional 'storage' section
            if 'storage' not in config:
                logger.warning(f"'storage' section not found in {CONFIG_FILE}. Using default file paths.")
                config['storage'] = default_storage_config
            else:
                 # Ensure storage is a dictionary
                 if not isinstance(config['storage'], dict):
                      logger.error(f"'storage' section in {CONFIG_FILE} must be a dictionary (key-value pairs).")
                      sys.exit(f"Error: Invalid 'storage' section in {CONFIG_FILE}. Exiting.")
                 # Check for specific paths within storage, providing defaults if missing
                 if 'transaction_file_path' not in config['storage']:
                      logger.warning(f"'transaction_file_path' missing in {CONFIG_FILE}['storage']. Using default: {DEFAULT_TRANSACTIONS_FILE}")
                      config['storage']['transaction_file_path'] = DEFAULT_TRANSACTIONS_FILE
                 if 'new_transaction_file_path' not in config['storage']:
                      logger.warning(f"'new_transaction_file_path' missing in {CONFIG_FILE}['storage']. Using default: {DEFAULT_NEW_TRANSACTIONS_FILE}")
                      config['storage']['new_transaction_file_path'] = DEFAULT_NEW_TRANSACTIONS_FILE

            logger.debug(f"Loaded configuration: {config}") # Log final config for debugging
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error parsing {CONFIG_FILE}: {e}")
        sys.exit(f"Error: Could not parse {CONFIG_FILE}. Exiting.")
    except IOError as e:
        logger.error(f"Could not read {CONFIG_FILE}: {e}")
        sys.exit(f"Error: Could not read {CONFIG_FILE}. Exiting.")
    except Exception as e:
        logger.error(f"Unexpected error loading {CONFIG_FILE}: {e}", exc_info=True)
        sys.exit(f"Error loading {CONFIG_FILE}. Exiting.")

def create_default_yaml(file_path, default_content):
     """Creates a default YAML file if it doesn't exist."""
     if not os.path.exists(file_path):
         logger.warning(f"{file_path} not found. Creating default file.")
         try:
             with open(file_path, 'w', encoding='utf-8') as file:
                 yaml.dump(default_content, file)
             logger.info(f"Default {file_path} created.")
         except IOError as e:
             logger.error(f"Could not create default {file_path}: {e}")
             # Optionally exit if this file is critical
             # sys.exit(f"Error creating {file_path}. Exiting.")

def main():
    """Main application entry point."""
    logger.info("Starting cmdbudget application...")
    
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
         logger.warning(f"Main transaction file '{transactions_file}' not found. Creating empty file with headers.")
         try:
             # Use TransactionOperations field names for consistency
             from transaction_operations import CSV_FIELDNAMES 
             with open(transactions_file, 'w', newline='', encoding='utf-8') as f:
                 writer = csv.writer(f)
                 writer.writerow(CSV_FIELDNAMES) 
             logger.info(f"Created empty transaction file: {transactions_file}")
         except IOError as e:
             logger.error(f"Could not create transaction file '{transactions_file}': {e}")
             sys.exit(f"Error creating {transactions_file}. Exiting.")
         except ImportError:
             logger.error("Could not import CSV_FIELDNAMES from transaction_operations. Cannot create transaction file header.")
             sys.exit("Initialization error. Exiting.")
         except Exception as e: # Catch other potential errors during file creation
             logger.error(f"Unexpected error creating transaction file '{transactions_file}': {e}", exc_info=True)
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
         # Catch broad exceptions during critical initialization
         logger.critical(f"Fatal error during application initialization or run: {e}", exc_info=True)
         print(f"\nA critical error occurred: {e}\nPlease check the application logs for more details.")
         sys.exit(1) # Exit with a non-zero code

if __name__ == "__main__":
    main()
