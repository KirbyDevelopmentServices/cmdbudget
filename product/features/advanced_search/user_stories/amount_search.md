# User Story: Search Transactions by Amount

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user tracking my finances, I want to search for transactions by amount ranges and currency, so that I can find specific transactions or analyze spending patterns for transactions of particular values.

## Acceptance Criteria
- Users can search for transactions with amounts greater than, less than, or equal to a specified value
- Users can search for transactions within a range of amounts (minimum to maximum)
- Amount searches respect the transaction's currency (e.g., 100 USD vs 100 CAD)
- Users can optionally specify which currency to search within
- Search allows for exact amount matching (e.g., exactly 49.99)
- Amount search can be combined with other search criteria
- Search results display the amount criteria used
- Results can be sorted by amount (ascending or descending)

## Notes
- Consider how to handle transactions with negative amounts (income vs. expense)
- Users often search for approximate amounts when they don't remember the exact value
- Support for formatting varies (e.g., "100", "$100", "100.00")
- Currency-specific searches are important for users who track multiple currencies 