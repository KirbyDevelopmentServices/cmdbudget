# cmdbudget Architecture

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

This document describes the architecture of the cmdbudget application, a terminal-based financial tracking tool for analyzing personal spending patterns. The system is designed as a modular Python application with several core components that work together to provide transaction management, categorization, and reporting functionality.

## System Overview

cmdbudget is a terminal-based application that allows users to:
1. Import transactions from CSV files exported from financial institutions
2. Categorize and tag transactions
3. View spending reports by month, category, or tag
4. Manage categories and transaction mappings

The application follows a modular design with clear separation of concerns between components. The architecture uses a command-line interface with menu-driven interactions, file-based storage, and no external database dependencies.

## Core Components

### 1. Main Application (main.py)

The main entry point that:
- Initializes configuration
- Creates default files if they don't exist
- Launches the CLI interface

The main module handles application startup, configuration loading, and validation. It ensures all required files exist before launching the main CLI loop.

### 2. Command Line Interface (cli.py)

Provides a menu-driven terminal interface with:
- Main menu
- Reporting submenu
- Transaction management submenu
- Category management submenu

The CLI module orchestrates user interaction through nested menus and delegates actual processing to specialized components. It focuses on collecting user input and directing control flow without implementing business logic directly.

### 3. Transaction Data Model (transaction.py)

Defines the core data structures:
- `BaseTransaction`: Abstract base class with core transaction properties
- `RawTransaction`: Imported CSV data before processing
- `Transaction`: Fully processed transaction with category information

The transaction module utilizes Python's dataclasses and abstract base classes to create a flexible type system for representing transactions at different stages of processing.

### 4. Transaction Processing (transaction_processor.py)

Handles the core business logic for:
- Importing transactions from CSV files
- Categorizing transactions based on mappings
- Prompting for manual categorization when needed
- Supporting transaction splitting
- Saving transaction mappings for future imports

The transaction processor contains a `TransactionClassifier` class for categorization logic and a `NewTransactionProcessor` class for handling the import workflow.

### 5. Transaction Operations (transaction_operations.py)

Provides low-level file operations:
- Reading transactions from CSV
- Writing transactions to CSV
- Creating new transaction objects
- Handling file I/O

This module acts as a data access layer, abstracting the details of CSV file reading and writing from the rest of the application.

### 6. Transaction Management (transactions_manager.py)

Coordinates operations between components:
- Initializes and maintains transaction data
- Groups transactions by month for reporting
- Manages categories and mappings
- Coordinates between processing and reporting

The transactions manager serves as a façade, providing a unified interface to transaction data for the CLI.

### 7. Transaction Editing (transactions_editor.py)

Handles transaction modification:
- Editing existing transactions
- Validation of edits
- Persistence of changes

### 8. Reporting (transaction_reporter.py)

Generates reports and displays:
- Monthly spending summaries
- Category-based reports
- Tag-based reports
- Data visualization in the terminal

### 9. Display (display.py)

Centralizes all terminal output:
- Consistent message formatting
- Menus and prompts
- Tables and reports
- Error and warning messages

This module ensures consistent user interaction throughout the application and facilitates potential UI changes.

### 10. User Input (user_input.py)

Handles specialized input prompts:
- Date entry with validation
- Amount entry with validation
- Text input with constraints

### 11. Utilities (utils.py)

Provides common utility functions:
- Date parsing with multiple format support
- Other shared helper functions

## Data Flow

1. **Transaction Import**:
   - User selects the import option in the CLI
   - `TransactionsManager` initiates the import process
   - `NewTransactionProcessor` reads the CSV file through `TransactionOperations`
   - Each row is converted to a `RawTransaction` object
   - `TransactionClassifier` attempts to categorize based on existing mappings
   - User is prompted to categorize transactions when necessary
   - Categorized transactions are converted to `Transaction` objects
   - `TransactionOperations` saves the processed transactions to the main transaction file

2. **Reporting**:
   - User selects a report type in the CLI
   - `TransactionsManager` retrieves the appropriate transactions
   - `TransactionReporter` processes the data for the selected report type
   - Results are displayed to the user through the `Display` class

3. **Category Management**:
   - User makes category changes in the CLI
   - `TransactionsManager` updates the categories file
   - Changes affect future transaction categorization

## Data Storage

The application uses file-based storage with no external database:

1. **Config Files (YAML)**:
   - `config.yml`: Application configuration
   - `categories.yml`: Category definitions
   - `transaction_mappings.yml`: Mapping rules for categorization

2. **Transaction Files (CSV)**:
   - `transactions.csv`: Main transaction store
   - `new_transactions.csv`: Temporary file for importing new transactions

## Configuration System

The application uses a layered configuration approach:
1. Default values hardcoded in the application
2. Values from configuration files
3. User input during runtime

Configuration is validated at startup to ensure all required settings are present.

## Error Handling

The application implements a centralized error handling strategy:
1. Lower-level components log errors with the Python logging module
2. User-facing errors are displayed through the `Display` class
3. Critical errors terminate the application with a specific exit code
4. Non-critical errors are reported to the user and the application continues when possible

## Design Patterns

Several design patterns are employed:

1. **Façade Pattern**: `TransactionsManager` provides a simplified interface to the complex subsystem of transaction operations.
2. **Factory Method Pattern**: `Transaction.from_row()` and `RawTransaction.from_row()` create objects from raw data.
3. **Command Pattern**: CLI menu options represent commands that can be executed.
4. **Strategy Pattern**: Different reporting strategies can be selected at runtime.
5. **Composition**: Components are composed together rather than using deep inheritance hierarchies.

## Extension Points

The architecture supports extension in several ways:

1. **New Report Types**: Adding new reports by extending `TransactionReporter`.
2. **New CSV Formats**: The configurable CSV import adapts to different bank formats.
3. **New Commands**: The menu-driven CLI can be extended with new options.
4. **Enhanced Categorization**: The classification system could be extended with machine learning.

## Future Architectural Considerations

Areas where the architecture could evolve:

1. **Database Storage**: Transitioning from file-based to a database for improved performance with large transaction volumes.
2. **Web Interface**: Adding a web-based UI as an alternative to the terminal interface.
3. **Multi-user Support**: Adding user accounts and data isolation.
4. **API Layer**: Implementing a REST API to enable mobile apps or third-party integrations.
5. **Plugin System**: Creating a formal plugin architecture for extensions.

## Conclusion

The cmdbudget architecture follows a modular design with clear separation of concerns. Components interact through well-defined interfaces, making it maintainable and extensible. The simple file-based storage model matches the personal-use nature of the application while providing sufficient performance for typical transaction volumes. 