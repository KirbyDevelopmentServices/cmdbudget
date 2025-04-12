# cmdbudget Roadmap

This document outlines the development roadmap for cmdbudget, organized by core feature areas. Items that have been completed are checked off.

## Transaction Importing

- [x] Import transactions from CSV files
- [x] Configure importer to work with different bank CSV formats
- [x] Map CSV columns to required fields (description, amount, date)
- [x] Set default currency and parameters
- [x] Duplicate detection during import
- [ ] Support for more date formats in imports (partially implemented)
- [ ] Bulk import from multiple CSV files
- [ ] Error handling for malformed CSV files
- [ ] Handle multi-currency amounts during import: Currently, if the configured `amount_column` is empty, the amount defaults to 0.0, even if another currency column (e.g., `USD$`) has the value. Need to detect and use the correct amount and currency.

## Transaction Management

- [x] View transactions by month
- [x] Edit transaction details (category, subcategory, tags)
- [x] Split transactions into multiple components
- [x] Add custom tags to transactions
- [x] Adding custom transactions
- [x] Custom file path for transactions.csv storage
- [ ] Tagging in custom transaction entry
- [ ] Merchant selection in custom transaction entry
- [ ] Merge similar transactions
- [ ] Delete transactions
- [ ] Undo recent changes
- [ ] Batch editing of multiple transactions
- [ ] Search and filter transactions
- [ ] Transaction archiving for older data

## Automatic Categorization

- [x] Custom categories and subcategories
- [x] On-the-fly category creation
- [x] Transaction mapping rules based on descriptions
- [x] Import categorization rules
- [ ] Rule prioritization
- [ ] Regular expression support in rules

## Transaction Reporting

- [x] Monthly spending reports
- [x] Percentage changes from previous periods
- [x] Category history analysis
- [x] Tag analysis
- [x] Multi-currency support (CAD/USD)
- [ ] Annual summary reports
- [ ] Visual charts and graphs
- [ ] Trend analysis
- [ ] Customizable reporting periods
- [ ] Complex reporting with filters

## Technical Improvements

- [x] Command-line interface
- [x] Transaction CRUD operations abstraction
- [x] Multi-format date parsing
- [ ] Comprehensive test suite
- [ ] Performance optimizations for large transaction sets
- [ ] Logging system

## Future Considerations

- [ ] Simple REST API for integration with other tools
- [ ] Terminal UI improvements (colors, interactive elements)
- [ ] Recurring transaction identification
