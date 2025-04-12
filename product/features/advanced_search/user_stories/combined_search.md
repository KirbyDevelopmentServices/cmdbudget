# User Story: Combined Search with Multiple Criteria

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user with complex analysis needs, I want to search for transactions using multiple criteria simultaneously, so that I can perform targeted financial analysis and find very specific transactions.

## Acceptance Criteria
- Users can combine any number of search criteria (date, amount, category, description, tags)
- Search interface clearly displays all active search criteria
- Multiple criteria are combined with AND logic by default (transactions must match all criteria)
- Advanced options allow for OR logic between certain criteria
- Users can save common search combinations for future use
- Search results display the complete set of criteria used
- Users can modify individual criteria without resetting the entire search
- Search results update dynamically as criteria are added or modified
- Clear indication of when no transactions match the combined criteria

## Notes
- Common combined searches include: "all restaurant expenses over $50 in the last 3 months" or "all travel-tagged purchases from specific vendors"
- Consider the order of operations and grouping when supporting complex logic (AND/OR combinations)
- Users may want to exclude certain criteria (NOT logic)
- The interface should remain usable even with many criteria active 