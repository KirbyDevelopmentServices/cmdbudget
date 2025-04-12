# User Story: Store Currency Information with Transactions

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who tracks expenses in multiple currencies, I want cmdbudget to properly store currency information with each transaction, so that I can maintain an accurate record of my spending in each currency and view historical data correctly.

## Acceptance Criteria
- All transactions are stored with their associated currency code
- Transaction CSV storage format includes a currency column
- Existing transaction data is migrated to include currency information (defaulting to the system's default currency)
- When viewing transaction lists, the currency is clearly displayed alongside the amount
- When editing a transaction, I can see and change its currency if needed
- Currency information is preserved when transactions are modified
- When adding transactions manually, I can specify the currency

## Notes
- The storage format should be backward compatible to prevent data loss
- Some users may want to convert historical transactions to specific currencies
- Currency display should follow standard conventions (currency code or symbol) 