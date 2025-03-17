from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Tuple
from tabulate import tabulate
import locale

# Set locale for proper currency formatting
locale.setlocale(locale.LC_ALL, '')

def category_grouping_factory():
    return {
        "spends": {
            "CAD": 0,
            "USD": 0
        },
        "subcategories": defaultdict(int)
    }

class TransactionCategoryGrouper:
    def __init__(self, transactions):
        # Filter out ignored transactions
        self.transactions = [t for t in transactions if t.category != "IGNORED"]

    def group(self):
        category_mapping = defaultdict(category_grouping_factory)
        for transaction in self.transactions:
            category_mapping[transaction.category]["spends"][transaction.currency.upper()] += transaction.amount

            if transaction.subcategory:
                category_mapping[transaction.category]["subcategories"][transaction.subcategory] += transaction.amount

        return category_mapping

class TransactionReporter:
    def __init__(self, transactions, month_grouped_transactions):
        # Filter out ignored and split transactions
        self.transactions = [t for t in transactions if t.category not in ["IGNORED", "SPLIT"]]
        # Filter month_grouped_transactions to remove ignored and split transactions
        self.month_grouped_transactions = {
            k: [t for t in v if t.category not in ["IGNORED", "SPLIT"]]
            for k, v in month_grouped_transactions.items()
        }

    def get_available_months(self) -> List[Tuple[int, int]]:
        """Returns a sorted list of (year, month) tuples."""
        return sorted(self.month_grouped_transactions.keys())

    def get_available_categories(self) -> List[str]:
        """Returns a sorted list of unique categories, excluding IGNORED."""
        categories = set(t.category for t in self.transactions)
        return sorted(cat for cat in categories if cat != "IGNORED")

    def get_available_tags(self) -> List[str]:
        """Returns a sorted list of unique tags, excluding empty tags."""
        tags = set(t.tag for t in self.transactions if t.tag)  # Only include non-empty tags
        return sorted(tags)

    def display_month_data(self, month: int, year: int, transactions: List):
        """Display spending data for a specific month."""
        category_grouped = TransactionCategoryGrouper(transactions).group()
        month_name = datetime(year, month, 1).strftime('%B %Y')
        
        print("\n" + "="*60)
        print(f"📊 Spending Report for {month_name}".center(60))
        print("="*60 + "\n")

        # Prepare data for tabulation
        table_data = []
        total_cad = 0
        total_usd = 0

        for category_name, spend_data in category_grouped.items():
            spends = spend_data["spends"]
            cad_amount = spends["CAD"]
            usd_amount = spends["USD"]
            total_cad += cad_amount
            total_usd += usd_amount

            # Only add categories with spending
            if cad_amount > 0 or usd_amount > 0:
                row = [
                    category_name,
                    f"${cad_amount:,.2f}" if cad_amount > 0 else "-",
                    f"${usd_amount:,.2f}" if usd_amount > 0 else "-"
                ]
                table_data.append(row)

                # Add subcategories if they exist
                subcategories = spend_data["subcategories"]
                if subcategories:
                    for subcat, amount in subcategories.items():
                        table_data.append([
                            f"  └─ {subcat}",
                            f"${amount:,.2f}" if amount > 0 else "-",
                            "-"
                        ])

        # Add totals row
        table_data.append([
            "TOTAL",
            f"${total_cad:,.2f}",
            f"${total_usd:,.2f}" if total_usd > 0 else "-"
        ])

        # Print the table
        print(tabulate(
            table_data,
            headers=["Category", "CAD", "USD"],
            tablefmt="pretty",
            colalign=("left", "right", "right")
        ))
        print("\n")

    def display_category_data(self, category: str):
        """Display spending for a specific category across all months."""
        print("\n" + "="*60)
        print(f"📈 Spending History for {category}".center(60))
        print("="*60 + "\n")

        table_data = []
        yearly_totals = defaultdict(lambda: defaultdict(float))

        for (year, month) in self.get_available_months():
            transactions = self.month_grouped_transactions[(year, month)]
            category_transactions = [t for t in transactions if t.category == category]
            
            if category_transactions:
                month_name = datetime(year, month, 1).strftime('%B %Y')
                currency_totals = defaultdict(float)
                
                for t in category_transactions:
                    currency_totals[t.currency] += t.amount
                    yearly_totals[year][t.currency] += t.amount

                row = [
                    month_name,
                    f"${currency_totals['CAD']:,.2f}" if currency_totals['CAD'] > 0 else "-",
                    f"${currency_totals['USD']:,.2f}" if currency_totals['USD'] > 0 else "-"
                ]
                table_data.append(row)

        # Add yearly subtotals
        if yearly_totals:
            table_data.append(["-" * 20, "-" * 15, "-" * 15])
            for year in sorted(yearly_totals.keys()):
                totals = yearly_totals[year]
                row = [
                    f"{year} Total",
                    f"${totals['CAD']:,.2f}" if totals['CAD'] > 0 else "-",
                    f"${totals['USD']:,.2f}" if totals['USD'] > 0 else "-"
                ]
                table_data.append(row)

        # Print the table
        print(tabulate(
            table_data,
            headers=["Month", "CAD", "USD"],
            tablefmt="pretty",
            colalign=("left", "right", "right")
        ))
        print("\n")

    def display_tag_data(self, tag: str):
        """Display spending for a specific tag across all months."""
        print("\n" + "="*60)
        print(f"🏷️  Spending History for Tag: {tag}".center(60))
        print("="*60 + "\n")

        table_data = []
        yearly_totals = defaultdict(lambda: defaultdict(float))

        for (year, month) in self.get_available_months():
            transactions = self.month_grouped_transactions[(year, month)]
            tag_transactions = [t for t in transactions if t.tag == tag]
            
            if tag_transactions:
                month_name = datetime(year, month, 1).strftime('%B %Y')
                currency_totals = defaultdict(float)
                category_totals = defaultdict(lambda: defaultdict(float))
                
                for t in tag_transactions:
                    currency_totals[t.currency] += t.amount
                    yearly_totals[year][t.currency] += t.amount
                    category_totals[t.category][t.currency] += t.amount

                # Add month header
                table_data.append([
                    month_name,
                    f"${currency_totals['CAD']:,.2f}" if currency_totals['CAD'] > 0 else "-",
                    f"${currency_totals['USD']:,.2f}" if currency_totals['USD'] > 0 else "-"
                ])

                # Add category breakdown
                for category, amounts in category_totals.items():
                    table_data.append([
                        f"  └─ {category}",
                        f"${amounts['CAD']:,.2f}" if amounts['CAD'] > 0 else "-",
                        f"${amounts['USD']:,.2f}" if amounts['USD'] > 0 else "-"
                    ])
                
                # Add spacing between months
                table_data.append(["", "", ""])

        # Remove last empty row
        if table_data and not any(table_data[-1]):
            table_data.pop()

        # Add yearly subtotals
        if yearly_totals:
            table_data.append(["-" * 20, "-" * 15, "-" * 15])
            for year in sorted(yearly_totals.keys()):
                totals = yearly_totals[year]
                row = [
                    f"{year} Total",
                    f"${totals['CAD']:,.2f}" if totals['CAD'] > 0 else "-",
                    f"${totals['USD']:,.2f}" if totals['USD'] > 0 else "-"
                ]
                table_data.append(row)

        if table_data:
            print(tabulate(
                table_data,
                headers=["Month/Category", "CAD", "USD"],
                tablefmt="pretty",
                colalign=("left", "right", "right")
            ))
        else:
            print("No transactions found with this tag.")
        print("\n")

    @staticmethod
    def _format_currency(amount: float, currency: str) -> str:
        """Helper method to format currency values."""
        if amount == 0:
            return "-"
        return f"${amount:,.2f} {currency}" 