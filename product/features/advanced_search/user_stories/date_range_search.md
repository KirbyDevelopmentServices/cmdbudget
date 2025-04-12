# User Story: Search Transactions by Date Range

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Description
As a user who tracks expenses over time, I want to search for transactions within custom date ranges, so that I can analyze my spending over specific periods that don't necessarily align with calendar months.

## Acceptance Criteria
- Users can specify a start date and end date for their search
- The search interface accepts various date formats (YYYY-MM-DD, DD/MM/YY, etc.)
- Relative date options are available (e.g., "last 30 days", "past 3 months", "year to date")
- Users can search by month name and year (e.g., "January 2023")
- Search results only include transactions within the specified date range
- Search results display the date range used for the search
- Results are sorted by date by default (newest or oldest first, user configurable)
- The date range can be combined with other search criteria

## Notes
- Users often need to analyze spending for non-standard periods (e.g., vacation periods, academic semesters, project durations)
- Consider intuitive shortcuts for common date ranges
- Default to a reasonable date range when no dates are specified
- Ensure clear error messages for invalid date formats or impossible ranges 