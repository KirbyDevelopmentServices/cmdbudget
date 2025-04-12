# AI generated and maintained by Claude 3.7 Sonnet
# This file centralizes display logic for user output.
# License: MIT

from tabulate import tabulate
from typing import List, Dict, Any, Optional
from .currency_utils import format_currency

class Display:
    """Handles formatting and printing output to the console for the user."""

    @staticmethod
    def header(text: str, level: int = 1):
        """Prints a formatted header."""
        if level == 1:
            print("\n" + "=" * 70)
            print(f"{text}".center(70))
            print("=" * 70 + "\n")
        elif level == 2:
            print("\n" + "-" * 50)
            print(f"{text}".center(50))
            print("-" * 50 + "\n")
        else:
            print(f"\n--- {text} ---") # Default simple header

    @staticmethod
    def message(text: str):
        """Prints a standard message."""
        print(text)

    @staticmethod
    def error(text: str):
        """Prints an error message."""
        # Could add color or prefix later
        print(f"Error: {text}")

    @staticmethod
    def warning(text: str):
        """Prints a warning message."""
        # Could add color or prefix later
        print(f"Warning: {text}")

    @staticmethod
    def menu_item(index: int, text: str):
        """Prints a formatted menu item."""
        print(f"{index}. {text}")

    @staticmethod
    def table(table_data: List[List[Any]], headers: List[str], tablefmt: str = "pretty", colalign: Optional[tuple] = None, config: Optional[Dict[str, Any]] = None):
        """Prints data in a table format using tabulate.
        
        Args:
            table_data: List of rows to display
            headers: List of column headers
            tablefmt: Table format (default: "pretty")
            colalign: Optional tuple of column alignments
            config: Optional configuration dictionary for currency formatting
        """
        if not table_data:
            Display.message("(No data to display)")
            return

        # Format currency amounts if config is provided
        if config is not None:
            formatted_data = []
            for row in table_data:
                formatted_row = []
                for i, value in enumerate(row):
                    if headers[i] == "Amount" and isinstance(value, (int, float)):
                        # Find the currency for this row
                        currency = "CAD"  # Default currency
                        for j, header in enumerate(headers):
                            if header == "Currency" and j < len(row):
                                currency = row[j]
                                break
                        formatted_row.append(format_currency(value, currency, config))
                    else:
                        formatted_row.append(value)
                formatted_data.append(formatted_row)
            table_data = formatted_data

        # Add bold formatting to headers using ANSI codes for pretty table
        formatted_headers = [f"\033[1m{h}\033[0m" for h in headers]
        print(tabulate(
            table_data,
            headers=formatted_headers,
            tablefmt=tablefmt,
            colalign=colalign
        ))
        print("\n") # Add a newline after the table

    @staticmethod
    def prompt(text: str) -> str:
        """Displays a prompt and gets user input."""
        # Ensures consistency if we want to format prompts later
        return input(text)

    @staticmethod
    def separator(char: str = '-', length: int = 50):
         """Prints a separator line."""
         print(char * length)

    @staticmethod
    def format_amount(amount: float, currency: str, config: Dict[str, Any]) -> str:
        """Format a currency amount according to the configuration.
        
        Args:
            amount: The amount to format
            currency: The currency code
            config: The configuration dictionary
            
        Returns:
            Formatted currency string
        """
        return format_currency(amount, currency, config) 