# AI generated and maintained by Gemini 2.5 Pro
# This file contains general utility functions.
# License: MIT

from datetime import datetime
from .config import INPUT_DATE_FORMATS

def parse_date_multi_format(date_str: str) -> datetime:
    """Parse date string in multiple formats."""
    for date_format in INPUT_DATE_FORMATS:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue

    raise ValueError(f"Unable to parse date: {date_str} with known formats.") 