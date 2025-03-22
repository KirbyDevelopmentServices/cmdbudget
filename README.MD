# cmdbudget

<!-- AI generated and maintained by claude-3.7-sonnet -->

> **Note:** This is a personal project by a full-time developer. I am building this project completely with the assistance of Claude 3.7 Sonnet (Anthropic) and working to improve collaboration between myself and AI. I'm pursuing this project to fulfill a personal need while radically improving my ability to use AI to augment my work. I coded the original implementation that did backwards looking reporting on transactions, but since then I let the AI do all the coding while refinine my workflow and prompts.

If you want to buy me a coffee, I like coffee -> [Link](https://buymeacoffee.com/kirbydevelopmentservices).

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
- **Multi-Currency Support**: Track and report on spending in multiple currencies (primarily CAD/USD)

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

Run the application using Poetry:

```bash
poetry run python cmdbudget/main.py
```

Or if you're already in the Poetry shell:

```bash
python cmdbudget/main.py
```

### First-time Setup

On first run, the application will automatically create default configuration files:
- `config.yml`: Contains CSV structure configuration
- `categories.yml`: Contains default categories
- `transaction_mappings.yml`: Initially empty, will store your category mapping rules

You may want to edit these files before importing transactions to match your specific needs.

### Importing Transactions

1. Place your bank's CSV export in the project directory as `new_transactions.csv`
2. Run the application and select the import option
3. Follow the prompts to categorize new transactions

## Configuration

### CSV Structure

Edit `config.yml` to match your bank's CSV export format:

```yaml
csv_structure:
  description_column: 'Description'  # Column containing transaction description
  amount_column: 'Amount'            # Column containing transaction amount
  date_column: 'Transaction Date'    # Column containing transaction date
  default_currency: 'CAD'            # Default currency
```

### Custom Categories

Edit `categories.yml` to define your own spending categories and subcategories.

---

## License

This project is licensed under the MIT License - see the LICENSE file for details.
