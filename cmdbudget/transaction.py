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
    _currency: str # Store the detected currency
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

    @property
    def currency(self) -> str:
        return self._currency

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
            # Extract config flags first for clarity
            expenses_positive = config.get('expenses_are_positive', True) # Default true
            date_col = config['date_column']
            desc_col_key = 'description_column' # Key name
            currency_columns = config.get('currency_columns', {'CAD': 'CAD$'})
            currency_priority = config.get('currency_priority', ['CAD'])
            default_currency = config.get('default_currency', 'CAD')

            date_val = date_parser(row[date_col])
            
            # --- Handle Description Column(s) ---
            desc_config = config[desc_col_key] # Get the config value (str or list)
            if isinstance(desc_config, list):
                desc_parts = [row.get(col_name, '').strip() for col_name in desc_config]
                desc_val = ' '.join(part for part in desc_parts if part)
            elif isinstance(desc_config, str):
                desc_val = row.get(desc_config, '').strip()
            else:
                logger.error(f"Configuration error: '{desc_col_key}' must be a string or a list, got {type(desc_config)}")
                raise TypeError(f"Configuration error: '{desc_col_key}' must be a string or a list, got {type(desc_config)}")

            # --- Handle Currency and Amount ---
            detected_currency = None
            amount_val = 0.0

            # Try each currency in priority order
            for currency in currency_priority:
                if currency not in currency_columns:
                    logger.warning(f"Currency '{currency}' in priority list not found in currency_columns. Skipping.")
                    continue

                amount_col = currency_columns[currency]
                amount_str = str(row.get(amount_col, '0.0')).replace('$', '').replace(',', '').strip()

                if amount_str and amount_str != '0.0':
                    try:
                        raw_amount_val = float(amount_str)
                        if raw_amount_val != 0.0:
                            detected_currency = currency
                            amount_val = raw_amount_val
                            break
                    except ValueError:
                        logger.warning(f"Could not convert amount '{amount_str}' to float for currency '{currency}'. Trying next currency.")

            # If no currency was detected, use default
            if detected_currency is None:
                detected_currency = default_currency
                logger.info(f"No valid amount found in any currency column. Using default currency: {default_currency}")

            # Adjust sign based on config
            if not expenses_positive:
                amount_val = -amount_val

        except KeyError as e:
            logger.error(f"Missing column '{e}' needed for RawTransaction creation in row: {row}")
            raise
        except ValueError as e:
            logger.error(f"Value error parsing data for RawTransaction in row: {row} - {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during RawTransaction.from_row: {e}", exc_info=True)
            raise

        return cls(
            _date=date_val,
            _description=desc_val,
            _amount=amount_val,
            _currency=detected_currency,
            _raw_data=row
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
    def from_raw(cls, raw: RawTransaction, category: str,
                subcategory: str = "", tag: str = "", merchant: str = "") -> 'Transaction':
        """Create a Transaction from a RawTransaction."""
        return cls(
            raw.date,
            raw.description,
            raw.amount,
            raw.currency, # Use the detected currency from RawTransaction
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
            date_val = date_parser(row["Transaction Date"])
            amount_val = float(row["Amount"])
            currency_val = row.get("Currency", "CAD") # Default to CAD if not present

            return cls(
                _date=date_val,
                _description=row["Description"],
                _amount=amount_val,
                currency=currency_val,
                category=row["Category"],
                subcategory=row["Subcategory"],
                tag=row["Tag"],
                merchant=row["Merchant"]
            )
        except KeyError as e:
            logger.error(f"Missing expected column '{e}' in stored transaction row: {row}")
            raise
        except ValueError as e:
            logger.error(f"Value error parsing stored transaction row: {row} - {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Transaction.from_row: {e}", exc_info=True)
            raise 