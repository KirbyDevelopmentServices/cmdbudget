from datetime import datetime
from transaction_processor import NewTransactionProcessor
from transaction_reporter import TransactionReporter
from transactions_manager import TransactionsManager

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
        print("\nAvailable months:")
        for i, (year, month) in enumerate(months, 1):
            print(f"{i}. {datetime(year, month, 1).strftime('%B %Y')}")
        
        while True:
            try:
                choice = int(input("\nSelect a month (number): "))
                if 1 <= choice <= len(months):
                    return months[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def display_category_menu(self):
        """Display available categories and let user select one."""
        categories = self.reporter.get_available_categories()
        print("\nAvailable categories:")
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        
        while True:
            try:
                choice = int(input("\nSelect a category (number): "))
                if 1 <= choice <= len(categories):
                    return categories[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def display_tag_menu(self):
        """Display available tags and let user select one."""
        tags = self.reporter.get_available_tags()
        if not tags:
            print("\nNo tags found in transactions.")
            return None
            
        print("\nAvailable tags:")
        for i, tag in enumerate(tags, 1):
            print(f"{i}. {tag}")
        
        while True:
            try:
                choice = int(input("\nSelect a tag (number): "))
                if 1 <= choice <= len(tags):
                    return tags[choice - 1]
                print("Invalid choice. Please try again.")
            except ValueError:
                print("Please enter a valid number.")

    def reporting_menu(self):
        """Handle reporting options."""
        while True:
            print("\nReporting Menu:")
            print("1. Display by month")
            print("2. Display by category")
            print("3. Display by tag")
            print("4. Back to main menu")
            
            choice = input("\nSelect an option: ")
            
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
                print("Invalid choice. Please try again.")

    def transaction_management_menu(self):
        """Handle transaction management options."""
        while True:
            print("\nTransaction Management Menu:")
            print("1. Process new transactions")
            print("2. Back to main menu")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                self.transactions_manager.process_new_transactions()
            
            elif choice == "2":
                break
            
            else:
                print("Invalid choice. Please try again.")

    def category_management_menu(self):
        """Handle category management options."""
        while True:
            print("\nCategory Management Menu:")
            print("1. List all categories")
            print("2. Add new category")
            print("3. Delete category")
            print("4. Back to main menu")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                categories = self.transactions_manager.get_categories()
                print("\nCurrent categories:")
                for category in sorted(categories):
                    print(f"- {category}")
            
            elif choice == "2":
                new_category = input("\nEnter new category name: ").strip()
                if new_category:
                    if self.transactions_manager.add_category(new_category):
                        print(f"Added category: {new_category}")
                    else:
                        print("Category already exists")
                else:
                    print("Category name cannot be empty")
            
            elif choice == "3":
                categories = self.transactions_manager.get_categories()
                print("\nSelect category to delete:")
                for i, category in enumerate(sorted(categories), 1):
                    print(f"{i}. {category}")
                
                try:
                    choice = int(input("\nEnter number (or 0 to cancel): "))
                    if 1 <= choice <= len(categories):
                        category_to_delete = sorted(categories)[choice - 1]
                        if self.transactions_manager.has_transactions_with_category(category_to_delete):
                            print(f"Cannot delete '{category_to_delete}' - category is in use")
                        else:
                            self.transactions_manager.delete_category(category_to_delete)
                            print(f"Deleted category: {category_to_delete}")
                    elif choice != 0:
                        print("Invalid choice")
                except ValueError:
                    print("Please enter a valid number")
            
            elif choice == "4":
                break
            
            else:
                print("Invalid choice. Please try again.")

    def run(self):
        """Run the main CLI loop."""
        print("Starting up...")
        self.initialize()
        
        while True:
            print("\nMain Menu:")
            print("1. Reporting")
            print("2. Manage Transactions")
            print("3. Manage Categories")
            print("4. Exit")
            
            choice = input("\nSelect an option: ")
            
            if choice == "1":
                self.reporting_menu()
            
            elif choice == "2":
                self.transaction_management_menu()
            
            elif choice == "3":
                self.category_management_menu()
            
            elif choice == "4":
                print("Goodbye!")
                break
            
            else:
                print("Invalid choice. Please try again.") 