# Personal Expense Tracker

A desktop application built with Python and Kivy that helps users track their daily expenses and manage their monthly budget.

## Features

### User Authentication
- Secure user registration and login system
- User-specific data storage
- Persistent sessions

### Expense Management
- Add up to 5 expenses at once
- Daily expense tracking
- Monthly budget monitoring
- Duplicate transaction prevention
- Real-time budget validation

### Transaction Views
- Daily transaction view
- Monthly transaction summary
- Organized date-wise transaction display
- Transaction editing capabilities

### User Interface
- Clean and intuitive interface
- Date-wise transaction organization
- Clear feedback messages
- Error handling with user-friendly notifications

## Technical Details

### Built With
- Python - Core programming language
- Kivy - GUI framework
- TinyDB - JSON document database

### Key Components
- `home.py` - Main expense entry and budget management
- `view.py` - Daily transaction viewer
- `monthly.py` - Monthly transaction summary
- `login.py` - User authentication
- Custom .kv files for UI layouts

### Database Structure
- User-specific JSON files
- Transaction schema includes:
  - Date
  - Expense name
  - Amount
  - Monthly budget

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python main.py
```

## Requirements
- Python 3.x
- Kivy
- TinyDB
- Other dependencies listed in requirements.txt

## Usage

1. **Registration/Login**
   - Register with a username and password
   - Login to access your expense tracker

2. **Adding Expenses**
   - Enter date (DD/MM/YYYY format)
   - Set monthly budget
   - Add expense name and amount
   - Click "Save" to store transactions

3. **Viewing Transactions**
   - Daily View: See transactions for a specific date
   - Monthly View: View all transactions for a month
   - Edit View: Modify existing transactions

4. **Budget Management**
   - Set monthly budget limits
   - Automatic validation against budget limits
   - Real-time feedback on budget status

## Features in Detail

### Budget Control
- Monthly budget setting
- Automatic validation before transaction entry
- Warning messages for budget exceeded

### Transaction Validation
- Duplicate transaction prevention
- Amount format validation
- Required field checking

### Data Organization
- Date-wise transaction grouping
- Monthly summaries
- Daily transaction details

## Project Structure
```
expense-tracker/
├── main.py
├── home.py
├── view.py
├── monthly.py
├── login.py
├── database/
├── assets/
│   ├── fonts/
│   └── images/
└── .kv files
```

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments
- Kivy framework documentation
- TinyDB documentation
