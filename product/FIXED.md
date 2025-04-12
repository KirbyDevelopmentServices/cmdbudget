# cmdbudget Bug Fix Log

<!-- AI generated and maintained by claude-3.7-sonnet -->

This document tracks bugs identified and fixed in the cmdbudget project. Each entry includes a description of the bug, root cause analysis, solution implemented, and any preventive measures added.

## Format

Each bug fix should be documented with:

## Bug Fixes

<!-- New bug fixes will be added here -->

## 2024-04-01
**Author:** Gemini 2.5 Pro

**Bug Description:**
Duplicate transactions (especially those marked `IGNORED`) were not being skipped during CSV import, even when they existed in `transactions.csv`.

**Root Cause Analysis:**
The issue stemmed from inconsistent date parsing. The flexible `parse_date_multi_format` function, when reading dates from `transactions.csv` (which were written in `%d/%m/%y` format), was incorrectly interpreting dates like `04/03/25` as April 3rd (due to trying `%m/%d/%y` first) instead of March 4th. This caused a mismatch with the date parsed from the input CSV (e.g., `3/4/2025` parsed as March 4th), leading the duplicate check (which relies on date, description, and amount) to fail.

**Solution Implemented:**
Modified `TransactionOperations.read_transactions` to use a dedicated internal function `parse_stored_date` that *only* uses `datetime.strptime(date_str, "%d/%m/%y")` when parsing dates from the internally stored `transactions.csv`. The flexible `parse_date_multi_format` is still used for parsing dates from the external input CSV. `Transaction.from_row` was also updated to accept this specific parser.

**Preventive Measures:**
Separated date parsing logic for internal storage vs. external input to ensure consistent interpretation based on known formats.

## 2024-04-11
**Author:** Claude 3.7 Sonnet

**Bug Description:**
The reporting feature was displaying months without transactions and incorrectly parsing dates from `transactions.csv`. The issue was caused by inconsistent date parsing between storage and input formats.

**Root Cause Analysis:**
1. The `transactions.csv` file uses a consistent `dd/mm/yy` format for storage
2. The `parse_date_multi_format` function in `utils.py` was trying multiple formats, starting with `mm/dd/yy`
3. This caused dates like "04/03/25" to be interpreted as April 3rd instead of March 4th
4. The incorrect date parsing led to:
   - Months being displayed without transactions
   - Incorrect transaction dates in reports
   - Future months appearing in the reporting menu

**Solution Implemented:**
1. Created a new `config.py` file to centralize date format configuration:
   - `STORAGE_DATE_FORMAT = "%d/%m/%y"` for consistent storage format
   - `INPUT_DATE_FORMATS` for flexible parsing of new transactions
2. Updated `transaction_operations.py` to:
   - Use `STORAGE_DATE_FORMAT` when reading/writing to `transactions.csv`
   - Use a dedicated `parse_stored_date` function for internal storage
3. Modified `utils.py` to use `INPUT_DATE_FORMATS` from config for flexible parsing

**Preventive Measures:**
1. Centralized date format configuration in `config.py`
2. Separated storage and input date parsing logic
3. Added clear documentation of date formats in configuration
4. Improved error messages for date parsing failures

**Related Changes:**
- Updated `README.md` to document the date format configuration
- Updated `ARCHITECTURE.md` to reflect the new configuration system
- Added logging for date parsing issues
