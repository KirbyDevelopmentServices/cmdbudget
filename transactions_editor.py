# AI generated and maintained by claude-3.7-sonnet
# This file handles editing and updating existing transactions
# License: MIT

import csv
from typing import Dict, List
from datetime import datetime
from transaction import Transaction
from transaction_operations import TransactionOperations

class TransactionEditor:
    def __init__(self, transactions_file: str, classifier):
        self.transactions_file = transactions_file
        self.classifier = classifier

    def edit_transaction(self, transaction: Transaction) -> bool:
        """Edit an existing transaction."""
        # Load all transactions
        transactions = self._load_transactions()
        
        # Find the transaction to edit
        for idx, t in enumerate(transactions):
            if (t.date == transaction.date and 
                t.description == transaction.description and 
                t.amount == transaction.amount):
                
                # Show edit options
                print("\nEdit Transaction:")
                print("1. Edit category/subcategory")
                print("2. Add/edit tag")
                print("3. Add/edit merchant")
                print("4. Split transaction")
                print("5. Cancel")

                try:
                    choice = int(input("\nSelect an option (1-5): "))
                    if choice == 1:
                        category, subcategory = self.classifier.prompt_for_category(t.description)
                        transactions[idx] = self._update_transaction(t, category=category, subcategory=subcategory)
                    elif choice == 2:
                        tag = input("Enter tag: ").strip()
                        transactions[idx] = self._update_transaction(t, tag=tag)
                    elif choice == 3:
                        merchant = input("Enter merchant: ").strip()
                        transactions[idx] = self._update_transaction(t, merchant=merchant)
                    elif choice == 4:
                        # Handle splitting existing transaction
                        if self._split_existing_transaction(t, transactions):
                            # Remove the original transaction as it's been split
                            transactions.pop(idx)
                    elif choice == 5:
                        return False
                    else:
                        print("Invalid choice")
                        return False

                    # Save all transactions back to file
                    self._save_transactions(transactions)
                    return True

                except ValueError:
                    print("Please enter a valid number")
                    return False

        print("Transaction not found")
        return False

    def _update_transaction(self, transaction: Transaction, **kwargs) -> Transaction:
        """Create a new transaction with updated fields."""
        # Create a dictionary of the transaction's current values
        transaction_dict = {
            "date": transaction.date,
            "description": transaction.description,
            "amount": transaction.amount,
            "currency": transaction.currency,
            "category": transaction.category,
            "subcategory": transaction.subcategory,
            "tag": transaction.tag,
            "merchant": transaction.merchant
        }
        
        # Update with any provided kwargs
        transaction_dict.update(kwargs)
        
        # Create and return new transaction
        return Transaction(**transaction_dict)

    def _split_existing_transaction(self, transaction: Transaction, all_transactions: List[Transaction]) -> bool:
        """Handle splitting an existing transaction."""
        # Mark original transaction as SPLIT
        split_transaction = self._update_transaction(transaction, category="SPLIT", subcategory="")
        all_transactions.append(split_transaction)
        
        remaining_amount = transaction.amount
        while remaining_amount > 0:
            print(f"\nRemaining amount to split: ${remaining_amount:.2f}")
            split_choice = input("Would you like to add another split? (y/n): ").lower()
            
            if split_choice != 'y':
                if remaining_amount > 0:
                    print(f"Warning: ${remaining_amount:.2f} of the transaction will be unaccounted for.")
                break
            
            while True:
                try:
                    split_amount = float(input("Enter split amount: $"))
                    if split_amount <= 0:
                        print("Amount must be positive.")
                    elif split_amount > remaining_amount:
                        print(f"Amount cannot exceed remaining amount (${remaining_amount:.2f})")
                    else:
                        break
                except ValueError:
                    print("Please enter a valid number.")
            
            split_description = input("Enter description for this split: ")
            category, subcategory = self.classifier.prompt_for_category(split_description)
            
            # Create split transaction
            split = Transaction(
                date=transaction.date,
                description=split_description,
                amount=split_amount,
                currency=transaction.currency,
                category=category,
                subcategory=subcategory,
                tag="",
                merchant=""
            )
            all_transactions.append(split)
            remaining_amount -= split_amount
        
        return True

    def _load_transactions(self) -> List[Transaction]:
        """Load all transactions from file."""
        transactions = []
        try:
            with open(self.transactions_file, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(Transaction.from_row(row, TransactionOperations.parse_date_multi_format))
        except FileNotFoundError:
            print(f"No transactions file found at {self.transactions_file}")
        return transactions

    def _save_transactions(self, transactions: List[Transaction]):
        """Save all transactions back to file."""
        with open(self.transactions_file, 'w', newline='') as file:
            if not transactions:
                return
            
            # Get fieldnames from first transaction
            fieldnames = [
                "Transaction Date", "Description", "Amount", "Currency",
                "Category", "Subcategory", "Tag", "Merchant"
            ]
            
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            
            for transaction in transactions:
                writer.writerow({
                    "Transaction Date": transaction.date.strftime("%m/%d/%y"),
                    "Description": transaction.description,
                    "Amount": str(transaction.amount),
                    "Currency": transaction.currency,
                    "Category": transaction.category,
                    "Subcategory": transaction.subcategory,
                    "Tag": transaction.tag,
                    "Merchant": transaction.merchant
                }) 