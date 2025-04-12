# cmdbudget

<!-- AI generated and maintained by claude-3.7-sonnet -->

> **Note:** This is a personal project by a full-time developer. I am building this project completely with the assistance of Claude 3.7 Sonnet (Anthropic) and working to improve collaboration between myself and AI. I'm pursuing this project to fulfill a personal need while radically improving my ability to use AI to augment my work. I coded the original implementation that did backwards looking reporting on transactions, but since then I let the AI do all the coding while refinine my workflow and prompts.

I like coffee. If you want to buy me a coffee -> [Link](https://buymeacoffee.com/kirbydevelopmentservices).

## Overview

cmdbudget is a terminal-based financial tracking tool designed to work with CSV exports from banks and other financial institutions. It enables users to categorize, track, and analyze personal spending over time without requiring complex setup or cloud services.

The tool is designed to be backward-looking, meaning it helps you understand where your money went rather than planning future expenses. This approach makes it ideal for users who want to gain insights into their spending patterns and make informed financial decisions.

## Core Features

### Transaction Management
- **Import New Transactions**: Easily import transactions from CSV files exported from your bank or financial institution
- **Automatic Categorization**: The system remembers how you've categorized similar transactions in the past and applies these rules automatically
- **Transaction Splitting**: Split single transactions into multiple components (e.g., split a grocery store purchase that included household items)
- **Manual Editing**: Edit transaction details including categories, subcategories, tags, and merchant information

### Categorization
- **Custom Categories & Subcategories**: Define your own financial categories and subcategories to match your budgeting needs
- **On-the-fly Creation**: Add new categories and subcategories during transaction import without interrupting your workflow
- **Transaction Mapping**: Create rules that automatically assign categories based on transaction descriptions

### Reporting
- **Monthly Reports**: View spending by category/subcategory with percentage changes from previous months
- **Category History**: Analyze spending in specific categories across all months
- **Tag Analysis**: Track and analyze tagged expenses (e.g., "vacation" or "work expenses")
- **Multi-Currency Support**: Import and manage transactions in multiple currencies with configurable formatting and priority
  - Define currency columns in your CSV files
  - Set currency priority for automatic detection
  - Customize currency formatting (symbol position, decimal places)
  - Default currency fallback

### Configuration
- **Flexible CSV Import**: Configure the importer to work with your bank's specific CSV format
- **Configurable Column Mappings**: Map CSV columns to required fields (description, amount, date)
- **Default Values**: Set default currency and other parameters to streamline imports

## Roadmap

For a detailed list of planned features and improvements, please see the [ROADMAP.md](ROADMAP.md) file in this repository.

## Getting Started (For Developers)

### Prerequisites

This project uses Poetry for dependency management. 

1. **Install Poetry**:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   Verify the installation:

   ```bash
   poetry --version
   ```

2. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/cmdbudget.git
   cd cmdbudget
   ```

### Installation

1. **Install dependencies using Poetry**:

   ```bash
   poetry install
   ```

   This will create a virtual environment and install all dependencies specified in `pyproject.toml`.

2. **Activate the Poetry virtual environment** (optional):

   ```bash
   poetry shell
   ```

### Running the Application

Run the application using the Poetry script:

```bash
poetry run cmdbudget
```

This command executes the main entry point defined in `pyproject.toml`.

Alternatively, if you have activated the Poetry shell (`poetry shell`), you can run:

```bash
cmdbudget
```

### First-time Setup

On first run, the application will automatically create default configuration files in the project's root directory:
- `config.yml`: Contains CSV structure configuration and file paths.
- `categories.yml`: Contains default categories
- `transaction_mappings.yml`: Initially empty, will store your category mapping rules

You may want to edit these files before importing transactions to match your specific needs.

### Importing Transactions

1. Place your bank's CSV export in the project directory. The default filename expected is `new_transactions.csv`, but this can be configured in `config.yml`.
2. Run the application (`poetry run cmdbudget`) and select the import option from the "Manage Transactions" menu.
3. Follow the prompts to categorize new transactions

## Configuration

The application uses YAML files for configuration. Default files are created on the first run if they don't exist.

### `config.yml` Structure

This file controls CSV import settings and storage locations. Edit it to match your bank's CSV export format and preferred storage path. All paths are relative to the project root unless an absolute path is given.

**Required Section:**

*   `import_csv_structure`: Defines how to read your bank's CSV.
    *   `description_column` (Required): Name of the column containing the transaction description, OR a list of column names to combine (using spaces).
    *   `amount_column` (Required): Name of the column containing the transaction amount.
    *   `date_column` (Required): Name of the column containing the transaction date.
    *   `default_currency` (Optional, defaults to 'CAD'): Default currency code.
    *   `expenses_are_positive` (Optional, defaults to `true`): Set `true` if expenses are positive numbers in your CSV, `false` if they are negative.
    *   `currency_columns` (Optional): Dictionary mapping currency codes to CSV column names.
    *   `currency_priority` (Optional): List of currency codes in order of priority for detection.
    *   `currency_formatting` (Optional): Configuration for currency display formatting.

**Optional Section:**

*   `storage`: Defines where transaction files are stored.
    *   `transaction_file_path` (Optional, defaults to 'transactions.csv'): Path to the main stored transaction file.
    *   `new_transaction_file_path` (Optional, defaults to 'new_transactions.csv'): Path to the CSV file used for imports.

**Example `config.yml`:**

```yaml
# REQUIRED section:
import_csv_structure:
  # Can be a single string or a list:
  # description_column: 'Transaction Details' 
  description_column:
    - 'Description 1'
    - 'Description 2'
  amount_column: 'CAD$'
  date_column: 'Transaction Date'
  default_currency: 'CAD' # Optional
  expenses_are_positive: false # Optional (set true/false based on your bank CSV)
  
  # Multi-currency configuration (Optional)
  currency_columns:
    CAD: "CAD$"
    USD: "USD$"
    EUR: "EUR€"
  currency_priority: ["CAD", "USD", "EUR"]
  currency_formatting:
    CAD:
      symbol: "$"
      position: "before"
      decimal_places: 2
    USD:
      symbol: "$"
      position: "before"
      decimal_places: 2
    EUR:
      symbol: "€"
      position: "after"
      decimal_places: 2

# OPTIONAL section (defaults shown):
storage:
  transaction_file_path: 'transactions.csv'
  new_transaction_file_path: 'new_transactions.csv'
```

For detailed information about multi-currency configuration, see [Currency Configuration](documentation/currency_configuration.md).

### `categories.yml`

Edit this file to define your custom spending categories and optional subcategories.

**Example `categories.yml`:**
```yaml
categories:
  Groceries:
    - Supermarket
    - Corner Store
  Entertainment:
    - Movies
    - Dining Out
    - Streaming Services
  Housing: [] # Example category with no subcategories yet
  # System categories (required, do not remove)
  IGNORED: [] 
  SPLIT: [] 
```

### `transaction_mappings.yml`

This file stores rules for automatic categorization based on transaction descriptions. The application populates this file as you categorize transactions and choose to save the mapping.

**Example `transaction_mappings.yml`:**
```yaml
mappings:
  'AMAZON PRIME VIDEO':
    category: Entertainment
    subcategory: Streaming Services
  'TIM HORTONS':
    category: Dining Out
    subcategory: Coffee
```

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
