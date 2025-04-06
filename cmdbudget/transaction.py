# AI generated and maintained by claude-3.7-sonnet
# This file defines the transaction data models
# License: MIT

from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod
import logging

# Assuming utils might be needed later, keep commented or remove if not
# from .utils import parse_date_multi_format

logger = logging.getLogger(__name__)

class BaseTransaction(ABC):
    """Abstract base class for all transactions."""
    
    @property
    @abstractmethod
    def date(self) -> datetime:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def amount(self) -> float:
        pass

    def __hash__(self):
        """Consistent hashing logic for all transaction types.

        Hashing uses date, description (stripped), and the *absolute* amount rounded to 2 decimal places.
        """
        # Use absolute amount for hashing to detect duplicates regardless of sign convention
        rounded_abs_amount = round(abs(self.amount), 2)
        return hash((
            self.date.date(),
            self.description.strip().lower(),
            rounded_abs_amount # Hash based on absolute value
        ))

    def __eq__(self, other):
        """Consistent equality checking for all transaction types.

        Equality uses date, description (stripped), and the *absolute* amount rounded to 2 decimal places.
        """
        if not isinstance(other, BaseTransaction):
            return False
        # Compare absolute rounded amounts for equality check
        return (
            self.date.date() == other.date.date() and
            self.description.strip().lower() == other.description.strip().lower() and
            round(abs(self.amount), 2) == round(abs(other.amount), 2) # Compare absolute values
        )

@dataclass(eq=False)
class RawTransaction(BaseTransaction):
    """Represents a transaction from an external source before categorization."""
    _date: datetime
    _description: str
    _amount: float # Stores the amount with sign based on config (positive for expense)
    _raw_data: dict # Optional: store original row data

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> float:
        return self._amount

    @classmethod
    def from_row(cls, row: dict, config: dict, date_parser) -> 'RawTransaction':
        """Create a RawTransaction from a CSV row using configuration.

        Assumes 'config' is the dictionary from the 'import_csv_structure' section.
        Parses amount based on config['expenses_are_positive'] flag.
        Stores amount sign consistently (positive = expense).
        Raises ValueError if date or amount parsing fails.
        Raises KeyError if required columns are missing.
        """
        try:
            # The `config` parameter *is* the import structure config
            # No need to access config['import_csv_structure'] again

            # Extract config flags first for clarity
            expenses_positive = config.get('expenses_are_positive', True) # Default true
            date_col = config['date_column']
            desc_col_key = 'description_column' # Key name
            amount_col = config['amount_column']

            date_val = date_parser(row[date_col])
            
            # --- Handle Description Column(s) ---
            desc_config = config[desc_col_key] # Get the config value (str or list)
            if isinstance(desc_config, list):
                # Combine descriptions from multiple columns
                # Use row.get(col_name, '') to avoid KeyError if a column is missing in a row
                desc_parts = [row.get(col_name, '').strip() for col_name in desc_config]
                desc_val = ' '.join(part for part in desc_parts if part) # Join non-empty parts with a space
            elif isinstance(desc_config, str):
                # Single description column
                desc_val = row.get(desc_config, '').strip() # Use get() for safety
            else:
                # Invalid config type
                logger.error(f"Configuration error: '{desc_col_key}' must be a string or a list, got {type(desc_config)}")
                raise TypeError(f"Configuration error: '{desc_col_key}' must be a string or a list, got {type(desc_config)}")
            # --- End Handle Description ---

            # Clean and parse amount to raw float
            amount_str = str(row.get(amount_col, '0.0')).replace('$', '').replace(',', '').strip() # Use get() with default
            # Handle empty string after cleaning - default to 0.0
            if not amount_str:
                 raw_amount_val = 0.0
                 # Log a warning if the original column wasn't actually empty, 
                 # but became empty after cleaning (e.g., just contained '$')
                 if row.get(amount_col):
                      logger.warning(f"Amount column '{amount_col}' contained non-numeric data '{row[amount_col]}' in row. Treating as 0.0. Row: {row}")
            else:
                try:
                    raw_amount_val = float(amount_str)
                except ValueError:
                     logger.error(f"Could not convert cleaned amount string '{amount_str}' to float for column '{amount_col}'. Row: {row}")
                     raise # Re-raise the ValueError to be caught by the processor

            # Adjust sign based on config: We want positive to represent an expense internally.
            # If expenses in the CSV are positive (flag=True), keep the sign.
            # If expenses in the CSV are negative (flag=False), negate the value.
            if not expenses_positive:
                # If expenses are negative in the CSV, a negative number is an expense.
                # We negate it to make it positive (our internal convention for expense).
                # A positive number in the CSV (income) becomes negative.
                amount_val = -raw_amount_val
            else:
                 # If expenses are positive in the CSV, a positive number is an expense (keep sign).
                 # A negative number (income) remains negative.
                 amount_val = raw_amount_val

        except KeyError as e:
             logger.error(f"Missing column '{e}' needed for RawTransaction creation in row: {row}")
             raise # Re-raise KeyError to be caught by the processor
        except ValueError as e:
             logger.error(f"Value error parsing data for RawTransaction in row: {row} - {e}")
             raise # Re-raise ValueError
        except Exception as e:
             logger.error(f"Unexpected error during RawTransaction.from_row: {e}", exc_info=True)
             raise # Re-raise unexpected errors

        return cls(
            _date=date_val,
            _description=desc_val,
            _amount=amount_val, # Store the adjusted-sign amount
            _raw_data=row # Store the original row data
        )

@dataclass(eq=False) # Use BaseTransaction __eq__ and __hash__
class Transaction(BaseTransaction):
    """Represents a fully processed transaction with category and other metadata."""
    _date: datetime
    _description: str
    _amount: float # Stores amount with sign (positive=expense)
    currency: str
    category: str
    subcategory: str
    tag: str
    merchant: str

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> float:
        return self._amount

    @classmethod
    def from_raw(cls, raw: RawTransaction, currency: str, category: str,
                subcategory: str = "", tag: str = "", merchant: str = "") -> 'Transaction':
        """Create a Transaction from a RawTransaction."""
        return cls(
            raw.date,
            raw.description,
            raw.amount, # Use the already correctly-signed amount from RawTransaction
            currency,
            category,
            subcategory,
            tag,
            merchant
        )

    @classmethod
    def from_row(cls, row: dict, date_parser) -> 'Transaction':
        """Create a Transaction from a stored CSV row.

        Assumes amount in storage is already correctly signed (positive = expense).
        Uses the provided date_parser function.
        """
        try:
            # Use the provided date parser
            date_val = date_parser(row["Transaction Date"])
            # Amount from our CSV should already be correctly signed (positive=expense)
            amount_val = float(row["Amount"])

            return cls(
                _date=date_val,
                _description=row["Description"],
                _amount=amount_val,
                currency=row["Currency"],
                category=row["Category"],
                subcategory=row["Subcategory"],
                tag=row["Tag"],
                merchant=row["Merchant"]
            )
        except KeyError as e:
            logger.error(f"Missing expected column '{e}' in stored transaction row: {row}")
            raise # Re-raise to be handled by read_transactions
        except ValueError as e:
             logger.error(f"Value error parsing stored transaction row: {row} - {e}")
             raise # Re-raise
        except Exception as e:
             logger.error(f"Unexpected error during Transaction.from_row: {e}", exc_info=True)
             raise # Re-raise unexpected errors 