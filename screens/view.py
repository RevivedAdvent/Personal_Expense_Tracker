from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from tinydb import TinyDB
from kivy.clock import Clock
from kivy.properties import StringProperty

class View(Screen):
    current_username = StringProperty('')
    
    def on_enter(self):
        """
        Fetch the current username and default date for transactions
        """
        try:
            # Get username from login screen
            self.current_username = self.manager.get_screen('login').username
            
            # Get default date from Home screen
            default_date = self.manager.get_screen('home').ids.date_input.text
            self.ids.date_input.text = default_date
            
            # Load transactions
            self.load_transactions()
        except Exception as e:
            print(f"Error fetching username: {e}")
            self.current_username = ''
    
    def load_transactions(self):
        """
        Load and display transactions for the specified date
        """
        # Clear any existing content
        for child in self.children[:]:
            if isinstance(child, ScrollView):
                self.remove_widget(child)
        
        # Check if username exists
        if not self.current_username:
            self.display_no_transactions("No user logged in")
            return
        
        # Get the date to filter
        filter_date = self.ids.date_input.text.strip()
        
        # Attempt to load transactions
        try:
            # Open user-specific transactions file
            db_path = f'database/{self.current_username}_transactions.json'
            db = TinyDB(db_path)
            
            # Filter transactions by date
            transactions = [t for t in db.all() if t.get('date') == filter_date]
            
            # If no transactions
            if not transactions:
                self.display_no_transactions(f"No transactions found for {filter_date}")
                return
            
            # Create scroll view
            scroll_view = ScrollView(
                size_hint=(0.5, 0.6),
                pos_hint={'center_x': 0.3, 'center_y': 0.45},
                bar_color = (0,0,0,1),
                bar_inactive_color = (0,0,0,0),
                bar_width = "5dp"
            )
            
            # Create layout for transactions
            layout = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                spacing=10,
                padding=10
            )
            layout.bind(minimum_height=layout.setter('height'))
            
            # Date header
            date_header = Label(
                text=f"Transactions on {filter_date}",
                size_hint_y=None,
                height=50,
                font_size='25sp',
                color=(0,0,0,1)
            )
            layout.add_widget(date_header)
            
            # Add transactions to layout
            total_amount = 0
            for transaction in transactions:
                expense = transaction.get('expense', 'N/A')
                amount = transaction.get('amount', 0)
                total_amount += amount
                
                transaction_label = Label(
                    text=f"Expense: {expense}\nAmount: ₹{amount:.2f}",
                    size_hint_y=None,
                    height=70,
                    font_size='20sp',
                    color=(0,0,0,1)
                )
                layout.add_widget(transaction_label)
            
            # Total amount footer
            total_label = Label(
                text=f"Total Expenses: ₹{total_amount:.2f}",
                size_hint_y=None,
                height=50,
                font_size='25sp',
                color=(0, 1, 0, 1)  # Green text for total
            )
            layout.add_widget(total_label)
            
            # Add layout to scroll view
            scroll_view.add_widget(layout)
            
            # Add scroll view to screen
            self.add_widget(scroll_view)
        
        except FileNotFoundError:
            self.display_no_transactions("No transactions file found")
        except Exception as e:
            print(f"Error loading transactions: {e}")
            self.display_no_transactions("Error loading transactions")
    
    def display_no_transactions(self, message):
        """
        Display a message when no transactions are found for 2 seconds, then disappear.
        """
        # Create and add a label for no transactions
        no_transactions_label = Label(
            text=message,
            color=(1, 0, 0, 1),  # Red color
            font_size='25sp',
            size_hint=(1, 0.2),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        self.add_widget(no_transactions_label)

        # Schedule the label to be removed after 2 seconds
        def remove_label(dt):
            if no_transactions_label in self.children:  # Check if it's still present
                self.remove_widget(no_transactions_label)

        Clock.schedule_once(remove_label, 2)  # Remove after 2 seconds