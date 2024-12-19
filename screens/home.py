from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from kivy.uix.label import Label
from kivy.clock import Clock
from tinydb import TinyDB
from datetime import datetime
import os

class Home(Screen):
    current_username = StringProperty('')

    def on_enter(self):
        """
        Called when the screen is entered. Fetch the username and set the budget.
        """
        try:
            self.current_username = self.manager.get_screen('login').username
            self.ids.date_input.text = self.get_today_date()

            # Fetch the budget from the settings database
            db_path = f'database/{self.current_username}_settings.json'
            os.makedirs('database', exist_ok=True)
            db = TinyDB(db_path)
            user_settings = db.all()

            if user_settings:
                # Existing user: Set the budget to their saved integer value
                self.ids.budget_input.text = str(int(user_settings[0].get('budget', 10000)))
            else:
                # New user: Set default budget to 10000
                self.ids.budget_input.text = "10000"
                db.insert({'budget': 10000})

            # Add a listener to the budget input field to save changes
            self.ids.budget_input.bind(text=self.on_budget_change)
        except Exception as e:
            print(f"Error initializing budget: {e}")

    def on_budget_change(self, instance, value):
        """
        Save the updated budget whenever the text field is changed.
        """
        try:
            new_budget = int(value)
            db_path = f'database/{self.current_username}_settings.json'
            db = TinyDB(db_path)
            db.truncate()  # Clear previous settings
            db.insert({'budget': new_budget})
        except ValueError:
            print("Invalid budget value entered.")
        except Exception as e:
            print(f"Error saving budget: {e}")

    def get_today_date(self):
        """
        Returns today's date in DD/MM/YYYY format
        """
        return datetime.now().strftime("%d/%m/%Y")

    def save_transactions(self):
        """
        Save transactions and update the budget if it's changed.
        """
        if not self.current_username:
            print("No username found. Cannot save transactions.")
            return

        # Get the updated budget
        try:
            new_budget = float(self.ids.budget_input.text)
        except (ValueError, AttributeError):
            self.display_message("Please enter a valid budget amount", (1, 0, 0, 1))
            return

        # Update the budget in the settings database
        try:
            db_path = f'database/{self.current_username}_settings.json'
            db = TinyDB(db_path)
            db.truncate()  # Clear previous settings
            db.insert({'budget': new_budget})
        except Exception as e:
            print(f"Error saving budget: {e}")

        # Process and save transactions
        transactions = []
        expense_dict = {}
        current_transaction_total = 0
        new_expenses = []

        for i in range(1, 6):
            expense = self.ids[f'expense{i}'].text.strip()
            amount = self.ids[f'amount{i}'].text.strip()

            if expense and amount:
                new_expenses.append(expense)
                try:
                    amount = float(amount)
                    current_transaction_total += amount
                    expense_dict[expense.lower()] = {
                        'date': self.ids['date_input'].text,
                        'expense': expense,
                        'amount': amount
                    }
                except ValueError:
                    print(f"Invalid amount for expense {i}")

        transactions = list(expense_dict.values())

        if not transactions:
            self.display_message("Please enter at least one expense and amount", (1, 0, 0, 1))
            return

        # Check for duplicate transactions
        has_duplicate, duplicate_name = self.check_duplicate_transactions(
            self.ids['date_input'].text,
            new_expenses
        )

        if has_duplicate:
            self.display_message(
                f"Transaction '{duplicate_name}' already exists for today, please use a different name",
                (1, 0, 0, 1)
            )
            return

        # Get the month/year from the date
        date = self.ids['date_input'].text
        month_year = "/".join(date.split("/")[1:])

        # Calculate current monthly total
        existing_monthly_total = self.get_monthly_total(month_year)

        # Check if this transaction would exceed the budget
        if existing_monthly_total + current_transaction_total > new_budget:
            self.display_message("Transaction failed: Monthly Budget Exceeded", (1, 0, 0, 1))
            return

        # If we get here, we're under budget - proceed with saving
        os.makedirs('database', exist_ok=True)

        # Create or open user-specific database file
        db_path = f'database/{self.current_username}_transactions.json'
        db = TinyDB(db_path)

        # Insert transactions
        db.insert_multiple(transactions)

        # Display success message
        self.display_message("Transaction saved successfully!", (0, 1, 0, 1))

        # Clear input fields after saving
        self.clear_transaction_fields()

    def get_monthly_total(self, month_year):
        """
        Calculate total expenses for a given month
        """
        if not self.current_username:
            return 0

        try:
            db_path = f'database/{self.current_username}_transactions.json'
            db = TinyDB(db_path)

            # Get all transactions
            monthly_total = 0
            for transaction in db.all():
                date = transaction.get('date', '')
                if date:
                    # Extract month/year from date (DD/MM/YYYY format)
                    transaction_month = "/".join(date.split("/")[1:])
                    if transaction_month == month_year:
                        monthly_total += transaction.get('amount', 0)

            return monthly_total
        except Exception as e:
            print(f"Error calculating monthly total: {e}")
            return 0

    def check_duplicate_transactions(self, date, expenses):
        """
        Check if any of the expenses already exist for the given date
        Returns tuple (bool, str) - (is_duplicate, duplicate_expense_name)
        """
        try:
            db_path = f'database/{self.current_username}_transactions.json'
            db = TinyDB(db_path)

            # Get all transactions for the date
            existing_transactions = [t for t in db.all() if t.get('date') == date]

            # Check each new expense against existing ones
            for expense in expenses:
                for existing in existing_transactions:
                    if expense.lower() == existing.get('expense', '').lower():
                        return True, expense

            return False, None

        except Exception as e:
            print(f"Error checking duplicates: {e}")
            return False, None

    def display_message(self, message, color):
        """
        Display a temporary message on the screen
        """
        # Remove any existing feedback labels
        for child in self.children[:]:
            if isinstance(child, Label) and child.text in [
                "Transaction saved successfully!", 
                "Please enter at least one expense and amount", 
                "Expense entries updated",
                "Transaction failed: Monthly Budget Exceeded",
                "Transaction already exists for today, please use a different name"
            ]:
                self.remove_widget(child)

        # Create new feedback label
        feedback_label = Label(
            text=message,
            color=color,
            font_size="25sp",
            size_hint=(0.5, 0.1),
            pos_hint={"center_x": 0.3, "y": 0.38}
        )
        self.add_widget(feedback_label)

        # Remove label after specified time
        duration = 3 if "error" in message.lower() or "failed" in message.lower() else 2
        Clock.schedule_once(lambda *args: self.remove_widget(feedback_label), duration)

    def clear_transaction_fields(self):
        """
        Clear all transaction input fields after saving
        """
        for i in range(1, 6):
            self.ids[f'expense{i}'].text = ''
            self.ids[f'amount{i}'].text = ''

        # Reset date to today
        self.ids['date_input'].text = self.get_today_date()
