# User Story: Configure Multi-Currency Settings

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who imports transaction data from various financial institutions, I want to configure how cmdbudget handles different currency columns in my CSV files, so that I can ensure all my transactions are properly imported with the correct currency information.

## Acceptance Criteria
- Configuration file allows defining a mapping between currency codes and their corresponding CSV column names
- Configuration specifies a default currency to use when no specific currency information is available
- Users can define currency column priority for cases when multiple currency columns have values
- Configuration supports specifying how to handle currency symbols and formatting in reports
- Configuration changes take effect without requiring changes to existing transaction data
- Clear documentation and examples are provided for currency configuration options
- Configuration validation catches common errors like duplicated column names

## Notes
- Some banks use column headers like "Amount (USD)" while others might use "USD_Amount" or "USD$"
- Default configuration should work reasonably well without extensive customization
- Configuration should be straightforward for users who primarily use a single currency
- Consider providing a configuration wizard or helper for initial setup

## TSA Analysis

### Complexity Assessment
**Score: 7**

This feature has a high complexity score due to several factors:
- It requires significant changes to the configuration system and CSV import logic
- It affects core transaction processing functionality
- It needs to handle various CSV formats with potentially complex currency column naming patterns
- It must maintain backward compatibility with existing transaction data
- It requires validation and error handling for ambiguous currency situations

### Architectural Impact
- **Components Affected**: 
  - `main.py` (configuration loading and validation)
  - `transaction.py` (currency handling in Transaction model)
  - `transaction_processor.py` (currency detection during import)
  - `transaction_operations.py` (CSV reading/writing with currency awareness)
  - `transaction_reporter.py` (currency formatting in reports)

- **Data Flow Changes**: 
  - CSV import process will need to detect the appropriate currency column based on configuration
  - Transaction creation will need to use the correct currency information
  - Reporting will need to respect currency formatting settings

- **Integration Points**: 
  - Configuration system (`config.yml`)
  - Transaction import workflow
  - Transaction data model
  - Reporting system

### Technical Blockers
- **Current CSV Column Handling**: The current implementation in `RawTransaction.from_row` only supports a single amount column specified in the configuration. As noted in CHANGELOG.AI, there's a temporary workaround that defaults to 0.0 when the configured amount column contains non-numeric data, but this doesn't properly handle multiple currency columns.
  
- **Currency-Specific Column Detection**: There's no existing mechanism to detect which currency column to use for a given transaction.

- **Configuration Complexity**: The current configuration validation is rigid and expects specific structure. Extending it to support the more complex currency mapping may require significant refactoring.

### Implementation Recommendations
- **Extend `import_csv_structure` Configuration**: Add a new `currency_columns` section to the configuration that maps currency codes to column names:
  ```yaml
  import_csv_structure:
    # existing fields...
    currency_columns:
      CAD: "CAD$"
      USD: "USD$"
    currency_priority: ["CAD", "USD"]  # Priority order for processing
    default_currency: "CAD"
  ```

- **Refactor `RawTransaction.from_row`**: Modify the method to check multiple currency columns according to the priority list, selecting the first non-empty value.

- **Add Currency Configuration Validation**: Extend `load_config()` in `main.py` to validate the currency configuration structure.

- **Create Currency Selection Logic**: Implement a function that determines which currency column to use for a given row based on configuration and available data.

- **Add Migration Support**: Ensure that users can migrate from the current model to the new currency-aware configuration without data loss.

### Technical Considerations
- **Performance**: Parsing multiple currency columns for each transaction may impact import performance slightly. Consider caching currency detection decisions when processing multiple rows from the same source.

- **Error Handling**: Add robust error handling for ambiguous currency situations, such as when multiple currency columns have values but no priority is specified.

- **Backward Compatibility**: The implementation must maintain backward compatibility with existing transaction data and configurations. Consider a migration path or automatic conversion.

- **Testing Approach**: Develop test cases for various CSV formats with different currency column patterns to ensure robust parsing.

### Related Changes
The CHANGELOG.AI reveals that there was already work done on April 1, 2024, regarding multi-currency issues:

> **Amount Parsing Workaround (Multi-Currency Issue):**
> - Modified `RawTransaction.from_row` to handle cases where the configured `amount_column` (e.g., `CAD$`) is empty or contains non-numeric data in the input CSV.
> - If the primary amount column is empty/invalid, the transaction amount defaults to `0.0` to prevent crashing during import.
> - **Reason:** Temporary workaround to allow import processing to continue when dealing with CSVs that have separate columns for different currencies (e.g., `CAD$`, `USD$`). The proper fix (detecting currency and amount from the correct column) is logged in `ROADMAP.md`.

This indicates that the current system is already facing issues with multi-currency support and has a temporary workaround in place. The new feature will provide a proper solution to replace this workaround.

## Technical Breakdown

### Requirements Context
- **User Story**: Configure Multi-Currency Settings
- **Acceptance Criteria**: 
  - Configuration file mapping between currency codes and CSV column names
  - Default currency specification
  - Currency column priority definition
  - Currency symbol and formatting configuration
  - Non-disruptive configuration changes
  - Documentation and examples
  - Configuration validation
- **TSA Analysis Reference**: Complexity Score 7, with architectural impacts on configuration system, CSV import logic, and core transaction processing

### Implementation Tasks
1. **Extend Configuration System**
   - Description: Add new currency configuration structure to config.yml
   - Dependencies: None
   - Effort: Medium
   - Files to Modify: 
     - `config.yml` (template)
     - `main.py` (configuration loading and validation)
   ```yaml
   import_csv_structure:
     currency_columns:
       CAD: "CAD$"
       USD: "USD$"
     currency_priority: ["CAD", "USD"]
     default_currency: "CAD"
   ```

2. **Update Configuration Validation**
   - Description: Add validation for new currency configuration structure
   - Dependencies: Task 1
   - Effort: Medium
   - Files to Modify:
     - `main.py` (load_config function)
     - `config_validation.py` (new validation rules)

3. **Refactor RawTransaction Class**
   - Description: Modify from_row method to handle multiple currency columns
   - Dependencies: Tasks 1, 2
   - Effort: High
   - Files to Modify:
     - `transaction.py` (RawTransaction class)
     - `transaction_processor.py` (currency detection logic)

4. **Implement Currency Selection Logic**
   - Description: Create function to determine which currency column to use
   - Dependencies: Tasks 1, 2
   - Effort: Medium
   - Files to Modify:
     - `transaction_processor.py` (new currency selection function)
     - `transaction.py` (integration with Transaction model)

5. **Add Currency Formatting Support**
   - Description: Implement currency symbol and formatting configuration
   - Dependencies: Tasks 1, 2
   - Effort: Medium
   - Files to Modify:
     - `transaction_reporter.py` (formatting logic)
     - `display.py` (currency display handling)

6. **Create Documentation**
   - Description: Add documentation for currency configuration
   - Dependencies: Tasks 1-5
   - Effort: Low
   - Files to Modify:
     - `docs/currency_configuration.md` (new documentation)
     - `README.md` (add reference to new documentation)

### Test Requirements
- **Unit Tests**:
  - Configuration validation for currency settings
  - Currency column detection and selection
  - Currency formatting in reports
  - Default currency fallback behavior
  - Priority-based currency selection

- **Integration Tests**:
  - End-to-end CSV import with multiple currency columns
  - Configuration changes without data loss
  - Currency formatting in different report types
  - Migration from old to new configuration

### Technical Context
- **Key Components**:
  - `RawTransaction`: Handles initial CSV row parsing and currency detection
  - `Transaction`: Core transaction model with currency information
  - `TransactionProcessor`: Manages currency selection and processing
  - `Config`: Handles currency configuration loading and validation
  - `TransactionReporter`: Formats currency values in reports

- **Implementation Patterns**:
  - Configuration-driven design for currency handling
  - Priority-based selection for ambiguous cases
  - Fallback to default currency when needed
  - Validation-first approach for configuration changes

### Edge Cases
- Multiple currency columns with values in the same row
- Missing currency columns in CSV
- Invalid currency codes in configuration
- Currency symbols in unexpected formats
- Configuration changes with existing transaction data
- CSV files with inconsistent currency column naming

### Integration Points
- CSV import workflow
- Transaction data model
- Configuration system
- Reporting system
- Display formatting
- Data validation

### Performance Considerations
- Caching currency detection decisions for same-source CSVs
- Efficient validation of currency configuration
- Optimized currency column lookup in CSV rows
- Memory usage with multiple currency columns

### Technical Debt Notes
- Current workaround in `RawTransaction.from_row` needs to be replaced
- Configuration validation needs refactoring for new structure
- Currency handling logic needs consolidation
- Documentation needs updating for new features 