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
