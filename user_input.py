# AI generated and maintained by Gemini 2.5 Pro
# This file contains utility functions for prompting user input.
# License: MIT

from datetime import datetime, date

def prompt_for_date() -> date:
    """Prompts the user for a transaction date, defaulting to today."""
    while True:
        date_str = input("Transaction Date (dd/mm/yyyy) [today]: ").strip()
        if not date_str:
            return date.today()  # Default to today
        try:
            # Use dd/mm/yyyy format specifically for manual entry consistency
            return datetime.strptime(date_str, "%d/%m/%Y").date()
        except ValueError:
            print("Invalid date format. Please use dd/mm/yyyy format.")

def prompt_for_description() -> str:
    """Prompts the user for a transaction description."""
    while True:
        description = input("Description: ").strip()
        if description:
            return description
        print("Description cannot be empty.")

def prompt_for_amount() -> float:
    """Prompts the user for a transaction amount."""
    while True:
        amount_str = input("Amount: $").strip()
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Amount must be positive.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

def prompt_for_currency() -> str:
    """Prompts the user to select a currency (CAD or USD)."""
    while True:
        print("\nSelect currency:")
        print("1. CAD")
        print("2. USD")
        currency_choice = input("Select currency [1]: ").strip()
        if not currency_choice or currency_choice == '1':
            return "CAD" # Default to CAD
        elif currency_choice == '2':
            return "USD"
        else:
            print("Invalid choice. Please select 1 or 2.")

# Potential future additions:
# def prompt_for_tag(): ...
# def prompt_for_merchant(): ... 