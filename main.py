import csv
import os
from datetime import datetime
from dataclasses import dataclass
from collections import defaultdict
from typing import Dict, List, TypedDict

TRANSACTIONS_FILE_NAME = "transactions.csv"


def category_grouping_factory():
    return {
        "spends": {
            "CAD": 0,
            "USD": 0
        },
        "subcategories": defaultdict(int)
    }


@dataclass
class Transaction:
    date: datetime
    description: str
    amount: int
    currency: str
    category: str
    subcategory: str
    tag: str
    merchant: str


class TransactionCategoryGrouper:

    def __init__(self, transactions):
        self.transactions = transactions


    def group(self):
        category_mapping = defaultdict(category_grouping_factory)
        for transaction in self.transactions:
            category_mapping[transaction.category]["spends"][transaction.currency.upper()] += transaction.amount

            if transaction.subcategory:
                category_mapping[transaction.category]["subcategories"][transaction.subcategory] += transaction.amount

        return category_mapping



class TransactionsProcessor:
    """Base class for processing bank statements."""
    
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_csv()

    def load_csv(self):
        """Reads the CSV file and returns its contents as a list of dictionaries."""
        try:
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                data = list(reader)
        except FileNotFoundError:
            print(f"Error: The file '{self.file_name}' was not found.")
        except Exception as e:
            print(f"Error reading file '{self.file_name}': {e}")
        else:
            return data

    def process(self):
        transactions = self.build_transactions()
        month_grouped_transaction = self.group_by_month(transactions)

        for (month, year), transactions in month_grouped_transaction.items():
            category_grouped_transactions = TransactionCategoryGrouper(transactions).group()
            self.display(month, year, category_grouped_transactions)

    def display(self, month, year, category_grouped_transactions):
        print(f"Displaying Date for {year} month {month}")
        for category_name, spend_data in category_grouped_transactions.items():
            print(f"Category: {category_name}")
            spends = spend_data["spends"]
            self.display_spends(spends)

        print("\n")

    def display_spends(self, spends):
        cad_spend = spends["CAD"]
        if cad_spend > 0:
            print(f"\tCAD total: {cad_spend}")

        usd_spend = spends["USD"]
        if usd_spend > 0:
            print(f"\tUSD total: {usd_spend}")
            



    def build_transactions(self):
        transactions = []

        for row in self.data:
            transaction = Transaction(
                self.parse_date(row["Transaction Date"]),
                row["Description 1"],
                int(float(row["Amount"])),
                row["Currency"],
                row["Category"],
                row["Subcategory"],
                row["Tag"],
                row["Merchant"]
            )
            transactions.append(transaction)

        return transactions

    def group_by_month(self, transactions):
        monthly_transaction_groups = defaultdict(list)

        for transaction in transactions:
            year_month_tuple = (transaction.date.year, transaction.date.month)
            monthly_transaction_groups[year_month_tuple].append(transaction)

        return monthly_transaction_groups


        # for category, total_spend in category_transaction_amount_mapping.items():
            # print(f"Category: {category} - ${total_spend}")

    @staticmethod
    def parse_date(date_str: str) -> datetime:
        return datetime.strptime(date_str, "%m/%d/%y")

def main():
    print("Starting up...")
    transactions_processor = TransactionsProcessor(TRANSACTIONS_FILE_NAME)
    transactions_processor.process()

if __name__ == "__main__":
    main()
