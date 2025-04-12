# User Story: Search Transactions by Description

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who wants to find specific transactions, I want to search for transactions by their description text, so that I can quickly locate purchases from specific merchants or for particular items.

## Acceptance Criteria
- Users can search for transactions containing specific text in the description
- Search supports partial word matching (e.g., searching for "market" finds "supermarket")
- Search is case-insensitive by default with an option for case-sensitive search
- Users can search for exact phrases with quotation marks
- Search supports basic wildcards and pattern matching
- Description search can be combined with other search criteria
- Search results highlight the matching text in descriptions
- Users can specify whether to match the beginning, end, or any part of the description
- Special characters in descriptions (like punctuation) don't prevent matching

## Notes
- Transaction descriptions often contain standardized text from financial institutions
- Many users remember part of a merchant name but not the exact format
- Consider offering suggestions for common merchant names during search
- Some descriptions contain non-standard characters or abbreviations 