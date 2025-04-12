# User Story: Import Transactions with Multiple Currencies

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who manages finances across multiple currencies, I want cmdbudget to correctly import transactions from CSV files that contain amounts in different currency columns, so that I can track all my spending accurately without manual data entry.

## Acceptance Criteria
- When importing a CSV with multiple currency columns, the system correctly detects and imports all transactions
- If the primary currency column is empty but another currency column has a value, the system uses that value and its associated currency
- When multiple currency columns have values for the same transaction, the system prioritizes based on configuration settings
- Configuration allows specifying a mapping between currency codes and their corresponding CSV column names
- Transactions are stored with their correct currency code
- The import process provides feedback on how many transactions were imported per currency
- Existing CSV files without currency information continue to work as before

## Notes
- A common scenario is bank CSV exports with separate columns for transactions in different currencies (e.g., USD$_amount, CAD$_amount)
- The default currency from configuration should be used when no currency information is available
- Some banks may use different column naming conventions for currency amounts 