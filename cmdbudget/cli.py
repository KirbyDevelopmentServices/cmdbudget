# AI generated and maintained by claude-3.7-sonnet
# This file implements the command-line interface
# License: MIT

from datetime import datetime
from .transaction_processor import NewTransactionProcessor
from .transaction_reporter import TransactionReporter
from .transactions_manager import TransactionsManager
from .display import Display

class BudgetCLI:
    def __init__(self, transactions_manager: TransactionsManager):
        self.transactions_manager = transactions_manager
        self.reporter = None

    def initialize(self):
        """Initialize the CLI with required data."""
        self.transactions_manager.initialize_data()
        self.reporter = self.transactions_manager.reporter

    def display_month_menu(self):
        """Display available months and let user select one."""
        months = self.reporter.get_available_months()
        Display.message("\nAvailable months:")
        for i, (year, month) in enumerate(months, 1):
            Display.menu_item(i, datetime(year, month, 1).strftime('%B %Y'))
        
        while True:
            try:
                choice_str = Display.prompt("\nSelect a month (number): ")
                choice = int(choice_str)
                if 1 <= choice <= len(months):
                    return months[choice - 1]
                Display.warning("Invalid choice. Please try again.")
            except ValueError:
                Display.warning("Please enter a valid number.")

    def display_category_menu(self):
        """Display available categories and let user select one."""
        categories = self.reporter.get_available_categories()
        Display.message("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            Display.menu_item(i, category)
        
        while True:
            try:
                choice_str = Display.prompt("\nSelect a category (number): ")
                choice = int(choice_str)
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                Display.warning("Invalid choice. Please try again.")
            except ValueError:
                Display.warning("Please enter a valid number.")

    def display_tag_menu(self):
        """Display available tags and let user select one."""
        tags = self.reporter.get_available_tags()
        if not tags:
            Display.message("\nNo tags found in transactions.")
            return None
            
        Display.message("\nAvailable tags:")
        for i, tag in enumerate(tags, 1):
            Display.menu_item(i, tag)
        
        while True:
            try:
                choice_str = Display.prompt("\nSelect a tag (number): ")
                choice = int(choice_str)
                if 1 <= choice <= len(tags):
                    return tags[choice - 1]
                Display.warning("Invalid choice. Please try again.")
            except ValueError:
                Display.warning("Please enter a valid number.")

    def reporting_menu(self):
        """Handle reporting options."""
        while True:
            Display.message("\nReporting Menu:")
            Display.menu_item(1, "Display by month")
            Display.menu_item(2, "Display by category")
            Display.menu_item(3, "Display by tag")
            Display.menu_item(4, "Back to main menu")
            
            choice = Display.prompt("\nSelect an option: ")
            
            if choice == "1":
                selected_month = self.display_month_menu()
                transactions = self.transactions_manager.get_transactions_for_month(selected_month)
                self.reporter.display_month_data(selected_month[1], selected_month[0], transactions)
            
            elif choice == "2":
                selected_category = self.display_category_menu()
                self.reporter.display_category_data(selected_category)
            
            elif choice == "3":
                selected_tag = self.display_tag_menu()
                if selected_tag:
                    self.reporter.display_tag_data(selected_tag)
            
            elif choice == "4":
                break
            
            else:
                Display.warning("Invalid choice. Please try again.")

    def transaction_management_menu(self):
        """Handle transaction management options."""
        while True:
            Display.message("\nTransaction Management Menu:")
            Display.menu_item(1, "Add a new transaction")
            Display.menu_item(2, "Process new transactions from new_transactions.csv")
            Display.menu_item(3, "Back to main menu")
            
            choice = Display.prompt("\nSelect an option: ")
            
            if choice == "1":
                self.transactions_manager.add_custom_transaction()
            
            elif choice == "2":
                self.transactions_manager.process_new_transactions()
            
            elif choice == "3":
                break
            
            else:
                Display.warning("Invalid choice. Please try again.")

    def category_management_menu(self):
        """Handle category management options."""
        while True:
            Display.message("\nCategory Management Menu:")
            Display.menu_item(1, "List all categories")
            Display.menu_item(2, "Add new category")
            Display.menu_item(3, "Delete category")
            Display.menu_item(4, "Back to main menu")
            
            choice = Display.prompt("\nSelect an option: ")
            
            if choice == "1":
                categories = self.transactions_manager.get_categories()
                Display.message("\nCurrent categories:")
                for category in sorted(categories):
                    Display.message(f"- {category}")
            
            elif choice == "2":
                new_category = Display.prompt("\nEnter new category name: ").strip()
                if new_category:
                    if self.transactions_manager.add_category(new_category):
                        Display.message(f"Added category: {new_category}")
                    else:
                        Display.warning("Category already exists")
                else:
                    Display.warning("Category name cannot be empty")
            
            elif choice == "3":
                categories = self.transactions_manager.get_categories()
                Display.message("\nSelect category to delete:")
                for i, category in enumerate(sorted(categories), 1):
                    Display.menu_item(i, category)
                
                try:
                    choice_str = Display.prompt("\nEnter number (or 0 to cancel): ")
                    choice = int(choice_str)
                    if 1 <= choice <= len(categories):
                        category_to_delete = sorted(categories)[choice - 1]
                        if self.transactions_manager.has_transactions_with_category(category_to_delete):
                            Display.warning(f"Cannot delete '{category_to_delete}' - category is in use")
                        else:
                            self.transactions_manager.delete_category(category_to_delete)
                            Display.message(f"Deleted category: {category_to_delete}")
                    elif choice != 0:
                        Display.warning("Invalid choice")
                except ValueError:
                    Display.warning("Please enter a valid number")
            
            elif choice == "4":
                break
            
            else:
                Display.warning("Invalid choice. Please try again.")

    def run(self):
        """Run the main CLI loop."""
        Display.message("Starting up...")
        self.initialize()
        
        while True:
            Display.message("\nMain Menu:")
            Display.menu_item(1, "Reporting")
            Display.menu_item(2, "Manage Transactions")
            Display.menu_item(3, "Manage Categories")
            Display.menu_item(4, "Exit")
            
            choice = Display.prompt("\nSelect an option: ")
            
            if choice == "1":
                self.reporting_menu()
            
            elif choice == "2":
                self.transaction_management_menu()
            
            elif choice == "3":
                self.category_management_menu()
            
            elif choice == "4":
                Display.message("Goodbye!")
                break
            
            else:
                Display.warning("Invalid choice. Please try again.") 