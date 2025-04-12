# User Story: Search Transactions by Tags

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who uses tags to organize transactions, I want to search for transactions by their assigned tags, so that I can analyze spending patterns across custom categories and track specific types of expenses.

## Acceptance Criteria
- Users can search for transactions that have specific tags assigned
- Search supports multiple tag selection (transactions with any of the selected tags)
- Users can search for transactions that have all specified tags (AND logic)
- Users can search for transactions that have no tags assigned
- Tag search can be combined with other search criteria
- Search results display the tag criteria used
- Results can be grouped by tag in the display
- Search results include options to summarize spending by tag
- Tags are presented in a way that makes selection easy (e.g., a list of existing tags)

## Notes
- Tags often represent cross-cutting concerns that don't fit into the main category hierarchy
- Users frequently use tags for projects, trips, family members, or temporary tracking needs
- Consider tag auto-completion based on existing tags in the system
- Some users create tags on-the-fly and may have inconsistent naming conventions 