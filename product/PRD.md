# cmdbudget Product Requirements Document

<!-- AI generated and maintained by Claude 3.7 Sonnet -->

## Product Vision

cmdbudget is a terminal-based financial tracking tool that helps users understand their past spending patterns through CSV import, categorization, and analysis of financial transactions from various institutions.

## User Personas

### Finance Tracker
- Wants to understand where money is being spent
- Exports transaction data from financial institutions
- Needs to categorize expenses and see patterns
- Prefers command-line tools over GUI applications

### Data Analyst
- Wants to extract insights from financial data
- Requires flexible reporting capabilities
- Needs to filter and search through transactions
- Values data integrity

## High-Level Requirements

### Core Functionality
- [✓] CSV import with configurable column mappings
- [✓] Transaction categorization system
- [✓] Monthly/category reporting
- [✓] Transaction editing capabilities
- [✓] Tag-based analysis
- [ ] Multi-currency support improvements
- [ ] Advanced search and filtering

### Upcoming Features

#### Multi-Currency Enhancement
Transform the existing basic multi-currency support into a comprehensive solution that properly handles transactions in different currencies during import, storage, and reporting.

#### Advanced Search System
Implement a flexible search system allowing users to find transactions using multiple criteria including date ranges, amounts, categories, descriptions, and tags.

## Feature Implementation Queue

1. Multi-Currency Enhancement
2. Advanced Search System

## Feature Breakdowns

The following features have been broken down into implementable units:

### Multi-Currency Enhancement

See detailed documentation in the [multi_currency](/product/features/multi_currency/) directory:
- [Feature Overview](/product/features/multi_currency/overview.md)
- [User Stories](/product/features/multi_currency/user_stories/)

### Advanced Search System 

See detailed documentation in the [advanced_search](/product/features/advanced_search/) directory:
- [Feature Overview](/product/features/advanced_search/overview.md)
- [User Stories](/product/features/advanced_search/user_stories/) 