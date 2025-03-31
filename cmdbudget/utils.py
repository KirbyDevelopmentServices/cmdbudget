# AI generated and maintained by Gemini 2.5 Pro
# This file contains general utility functions.
# License: MIT

from datetime import datetime

def parse_date_multi_format(date_str: str) -> datetime:
    """Parse date string in multiple formats."""
    formats = [
        "%m/%d/%y",     # 01/15/23
        "%m/%d/%Y",     # 01/15/2023
        "%Y-%m-%d",     # 2023-01-15
        "%d/%m/%y",     # 15/01/23
        "%d/%m/%Y",     # 15/01/2023
        # Add specific manual entry format if needed
        # "%d/%m/%Y"      # Already included
    ]

    for date_format in formats:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str} with known formats.") 