# AI generated and maintained by claude-3.7-sonnet
# This file defines the transaction data models
# License: MIT

from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod

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
    def amount(self) -> int:
        pass

    def __hash__(self):
        """Consistent hashing logic for all transaction types."""
        return hash((
            self.date,
            self.description.strip(),
            self.amount
        ))

    def __eq__(self, other):
        """Consistent equality checking for all transaction types."""
        if not isinstance(other, BaseTransaction):
            return False
        return (
            self.date == other.date and
            self.description.strip() == other.description.strip() and
            self.amount == other.amount
        )

@dataclass(eq=False)
class RawTransaction(BaseTransaction):
    """Represents a transaction from an external source before categorization."""
    _date: datetime
    _description: str
    _amount: int

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> int:
        return self._amount

    @classmethod
    def from_row(cls, row: dict, config: dict, date_parser) -> 'RawTransaction':
        """Create a RawTransaction from a CSV row using configuration."""
        return cls(
            date_parser(row[config['date_column']]),
            row[config['description_column']],
            int(float(row[config['amount_column']]))
        )

@dataclass(eq=False)
class Transaction(BaseTransaction):
    """Represents a fully processed transaction with category and other metadata."""
    _date: datetime
    _description: str
    _amount: int
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
    def amount(self) -> int:
        return self._amount

    @classmethod
    def from_raw(cls, raw: RawTransaction, currency: str, category: str, 
                subcategory: str = "", tag: str = "", merchant: str = "") -> 'Transaction':
        """Create a Transaction from a RawTransaction."""
        return cls(
            raw.date,
            raw.description,
            raw.amount,
            currency,
            category,
            subcategory,
            tag,
            merchant
        )

    @classmethod
    def from_row(cls, row: dict, date_parser) -> 'Transaction':
        """Create a Transaction from a CSV row."""
        return cls(
            date_parser(row["Transaction Date"]),
            row["Description"],
            int(float(row["Amount"])),
            row["Currency"],
            row["Category"],
            row["Subcategory"],
            row["Tag"],
            row["Merchant"]
        ) 