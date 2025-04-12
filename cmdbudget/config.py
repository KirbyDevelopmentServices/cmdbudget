# AI generated and maintained by claude-3.7-sonnet
# This file contains configuration constants for the application
# License: MIT

# Date format for transactions.csv storage
STORAGE_DATE_FORMAT = "%d/%m/%y"  # e.g., 15/01/23

# Date formats for input parsing (in order of priority)
INPUT_DATE_FORMATS = [
    "%d/%m/%y",     # 15/01/23
    "%d/%m/%Y",     # 15/01/2023
    "%m/%d/%y",     # 01/15/23
    "%m/%d/%Y",     # 01/15/2023
    "%Y-%m-%d",     # 2023-01-15
]

# CSV fieldnames for transactions.csv
CSV_FIELDNAMES = [
    "Transaction Date", "Description", "Amount", "Currency",
    "Category", "Subcategory", "Tag", "Merchant"
] 