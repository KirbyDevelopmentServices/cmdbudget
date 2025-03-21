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
        """Display spending data for a specific month with percentage changes."""
        # Get previous month's data
        prev_month = month - 1 if month > 1 else 12
        prev_year = year if month > 1 else year - 1
        prev_transactions = self.month_grouped_transactions.get((prev_year, prev_month), [])
        
        # Group current and previous month's transactions
        current_grouped = TransactionCategoryGrouper(transactions).group()
        prev_grouped = TransactionCategoryGrouper(prev_transactions).group()
        
        month_name = datetime(year, month, 1).strftime('%B %Y')
        prev_month_name = datetime(prev_year, prev_month, 1).strftime('%B %Y')
        
        print("\n" + "="*70)
        print(f"📊 Spending Report for {month_name}".center(70))
        print(f"(compared to {prev_month_name})".center(70))
        print("="*70 + "\n")

        # Prepare data for tabulation
        table_data = []
        totals = {"CAD": 0, "USD": 0}
        prev_totals = {"CAD": 0, "USD": 0}

        def format_amount_with_change(current: float, previous: float) -> str:
            """Format amount with percentage change in smaller font."""
            if current == 0:
                return "-"
            
            amount_str = f"${current:,.2f}"
            
            if previous == 0:
                pct_str = " (\033[2m∞\033[0m)" if current > 0 else ""
            else:
                pct_change = ((current - previous) / previous) * 100
                sign = "+" if pct_change > 0 else ""
                pct_str = f" (\033[2m{sign}{pct_change:.1f}%\033[0m)"
            
            return amount_str + pct_str

        # Get all categories from both months
        all_categories = set(current_grouped.keys()) | set(prev_grouped.keys())
        
        first_category = True
        for category_name in sorted(all_categories):
            if not first_category:
                # Add separator between categories
                table_data.append(["-" * 20, "-" * 25, "-" * 25])
            else:
                first_category = False

            current_data = current_grouped.get(category_name, {"spends": {"CAD": 0, "USD": 0}, "subcategories": {}})
            prev_data = prev_grouped.get(category_name, {"spends": {"CAD": 0, "USD": 0}, "subcategories": {}})
            
            current_spends = current_data["spends"]
            prev_spends = prev_data["spends"]
            
            # Calculate category totals
            cad_amount = current_spends["CAD"]
            prev_cad = prev_spends["CAD"]
            usd_amount = current_spends["USD"]
            prev_usd = prev_spends["USD"]
            
            totals["CAD"] += cad_amount
            totals["USD"] += usd_amount
            prev_totals["CAD"] += prev_cad
            prev_totals["USD"] += prev_usd
            
            if cad_amount > 0 or prev_cad > 0 or usd_amount > 0 or prev_usd > 0:
                # Add category with bold formatting
                table_data.append([
                    f"\033[1m{category_name}\033[0m",
                    format_amount_with_change(cad_amount, prev_cad),
                    format_amount_with_change(usd_amount, prev_usd)
                ])

                # Add subcategories
                current_subcats = current_data["subcategories"]
                prev_subcats = prev_data["subcategories"]
                all_subcats = set(current_subcats.keys()) | set(prev_subcats.keys())
                
                for subcat in sorted(all_subcats):
                    current_sub_amount = current_subcats.get(subcat, 0)
                    prev_sub_amount = prev_subcats.get(subcat, 0)
                    
                    if current_sub_amount > 0 or prev_sub_amount > 0:
                        table_data.append([
                            f"  └─ {subcat}",
                            format_amount_with_change(current_sub_amount, prev_sub_amount),
                            "-"  # Assuming subcategories are only in primary currency
                        ])

        # Add separator before total
        table_data.append(["=" * 20, "=" * 25, "=" * 25])

        # Add totals row with bold formatting
        table_data.append([
            "\033[1mTOTAL\033[0m",
            format_amount_with_change(totals["CAD"], prev_totals["CAD"]),
            format_amount_with_change(totals["USD"], prev_totals["USD"])
        ])

        # Print the table
        print(tabulate(
            table_data,
            headers=["\033[1mCategory\033[0m", "\033[1mCAD\033[0m", "\033[1mUSD\033[0m"],
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