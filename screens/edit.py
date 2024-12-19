from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from tinydb import TinyDB, Query
from datetime import datetime
import os

class Edit(Screen):
    def on_enter(self):
        """
        Set the date input to today's date when screen is entered
        """
        self.ids['date_input'].text = self.get_today_date()
    
    def get_today_date(self):
        """
        Returns today's date in DD/MM/YYYY format
        """
        return datetime.now().strftime("%d/%m/%Y")
    
    def display_message(self, message, color):
        """
        Display a temporary message on the screen
        """
        # Remove any existing feedback labels
        for child in self.children[:]:
            if isinstance(child, Label) and message in child.text:
                self.remove_widget(child)
        
        # Create new feedback label
        feedback_label = Label(
            text=message,
            color=color,
            font_size="25sp",
            size_hint=(0.5, 0.1),
            pos_hint = {"center_x": 0.3, "y": 0.8}
        )
        self.add_widget(feedback_label)
        
        # Remove label after 2 seconds
        Clock.schedule_once(lambda *args: self.remove_widget(feedback_label), 2)
    
    def update_expense(self):
        """
        Update an existing expense entry based on expense name and date
        """
        # Get input values
        old_expense = self.ids['old_expense_input'].text.strip()
        new_expense = self.ids['new_expense_input'].text.strip()
        new_amount = self.ids['new_amount_input'].text.strip()
        search_date = self.ids['date_input'].text.strip()
        
        # Validate inputs
        if not old_expense or not search_date:
            self.display_message("Please enter existing expense and date", (1, 0, 0, 1))
            return
        
        # If new expense is not provided, use the old expense
        if not new_expense:
            new_expense = old_expense
        
        # Validate amount if provided
        if new_amount:
            try:
                new_amount = float(new_amount)
            except ValueError:
                self.display_message("Invalid amount. Please enter a number.", (1, 0, 0, 1))
                return
        
        # Get username from login screen
        try:
            username = self.manager.get_screen('login').username
        except Exception as e:
            print(f"Error fetching username: {e}")
            self.display_message("User not found", (1, 0, 0, 1))
            return
        
        # Path to user's database
        db_path = f'database/{username}_transactions.json'
        
        # Check if database exists
        if not os.path.exists(db_path):
            self.display_message("No transactions found", (1, 0, 0, 1))
            return
        
        # Open the database
        db = TinyDB(db_path)
        
        # Create a query to find the expense
        query = Query()
        
        # Prepare update data
        update_data = {}
        if new_expense:
            update_data['expense'] = new_expense
        if new_amount:
            update_data['amount'] = new_amount
        
        # Find and update the expense (case-insensitive) for the specific date
        updated = db.update(
            update_data, 
            (query.expense.test(lambda x: x.lower() == old_expense.lower())) & 
            (query.date == search_date)
        )
        
        # Check if update was successful
        if updated:
            # Clear input fields
            self.ids['old_expense_input'].text = ''
            self.ids['new_expense_input'].text = ''
            self.ids['new_amount_input'].text = ''
            
            # Display success message
            self.display_message("Expense updated successfully!", (0, 1, 0, 1))
        else:
            # Display error if no matching expense found
            self.display_message("No matching expense found for the given date", (1, 0, 0, 1))