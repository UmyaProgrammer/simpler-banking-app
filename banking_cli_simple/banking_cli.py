from typing import Optional
# Pulling in the actual database work from your other file
from users import create_user, get_user, user_deposit, user_get_balance, user_withdraw, admin_get_users, get_all_transactions, create_transaction

# Hardcoded admin credentials for the portal
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

class BankingService:
    def __init__(self):
        # We don't need to store anything here since the database 
        # handles the "memory" of the app
        pass

    def signup(self, username: str, password: str, initial_deposit: float):
        # --- Validation Rules ---
        if not username.strip():
            return False, 'Name cannot be empty.'
        if len(password) < 4:
            return False, 'Password must be at least 4 characters.'
        if initial_deposit < 0:
            return False, 'Initial deposit cannot be negative.'

        create_user(username, password, initial_deposit)
        return True, 'Account created successfully.'

    def login(self, username: str, password: str):
        # Try to find the user dictionary in the DB
        user = get_user(username)

        if user == None:
            return None, 'Account not found.'
        
        # Check the password (Note: in a real app, we'd hash these!)
        if user['password_hash'] != password:
            return None, 'Incorrect password.'
        
        # Success! Return the user data to the UI
        return user, 'Login successful.'

    def deposit(self, username: str, amount: float):
        # Basic sanity check
        if amount <= 0:
            return False, 'Deposit amount must be greater than 0.'
        
        # Tell the database to update the balance and send back the new total
        new_balance = user_deposit(username, amount)
        create_transaction(username, "Deposit", amount)
            
        return True, f'Deposit successful. New balance: ${new_balance}'

    def withdraw(self, username: str, amount: float):
        if amount <= 0:
            return False, 'Withdrawal amount must be greater than 0.'
        
        # Rule: You can't spend money you don't have
        if user_get_balance(username) < amount:
            return False, 'Insufficient balance.'
        else:
            # Tell the DB to subtract the money
            new_balance = user_withdraw(username, amount)
            create_transaction(username, "Withdraw", amount)
            
        return True, f'Withdrawal successful. New balance: ${new_balance}'

    def get_balance(self, username: str):
        # Simple passthrough to the database function
        return user_get_balance(username)

    def list_all_accounts(self):
        # Grabs the list of dictionaries for the admin
        return admin_get_users()
    
    def list_all_transactions(self):
        # Returns a list of all the transactions
        return get_all_transactions()

# --- Simple Terminal UI ---

def read_float(prompt: str) -> Optional[float]:
    """Helper to catch typos when entering money amounts"""
    try:
        val = input(prompt).strip()
        return float(val) if val else None
    except ValueError:
        print('Error: Enter a valid number.')
        return None

def user_dashboard(service: BankingService, username: str) -> None:
    """The menu a user sees after they log in"""
    while True:
        print(f'\n--- USER: {username} ---')
        print('1. Deposit | 2. Withdraw | 3. Balance | 4. Logout')
        choice = input('Choice: ').strip()

        if choice == '1':
            amt = read_float('Amount: $')
            if amt: print(service.deposit(username, amt)[1])
        elif choice == '2':
            amt = read_float('Amount: $')
            if amt: print(service.withdraw(username, amt)[1])
        elif choice == '3':
            # Format the float to look like money ($0.00)
            print(f'Current Balance: ${service.get_balance(username):.2f}')
        elif choice == '4':
            break

def admin_portal(service: BankingService) -> None:
    """The master view for bank admins"""
    while True:
        print('\n--- ADMIN PORTAL ---')
        print('1. List All Users | 2. List All Transactions | 3. Exit')
        admin_input = input('Choice: ')
        if admin_input == '1':
            # Iterate through the list of dictionaries returned by the DB
            for row in service.list_all_accounts():
                print(f"User: {row['name']} | Balance: ${row['balance']:.2f}")
        elif admin_input == '2':
            for row in service.list_all_transactions():
                print(f"User: {row['user_id']} | Type: {row['type']} | amount: ${row['amount']} | Date: {row['created_at']}")
        else:
            break

def main():
    """The main entry point of the application"""
    service = BankingService()
    while True:
        print('\n=== BANK MAIN MENU ===')
        print('1. Login | 2. Signup | 3. Admin | 4. Exit')
        c = input('Choice: ')
        
        if c == '1':
            u, p = input('User: '), input('Pass: ')
            acc, msg = service.login(u, p)
            print(msg)
            if acc: user_dashboard(service, u) # Send them to the dashboard if login works
            
        elif c == '2':
            u= input('New User: ')
            existing_user = get_user(u)

            if existing_user is not None:
                print('An account with that name already exists.')
            else:
                p = input('New Pass: ')
                d = read_float('Initial $: ')
                if d is not None: print(service.signup(u, p, d)[1])
            
        elif c == '3':
            # Simple admin login check
            if input('Admin User: ') == ADMIN_USERNAME and input('Admin Pass: ') == ADMIN_PASSWORD:
                admin_portal(service)
            else:
                print("Access Denied.")
                
        elif c == '4':
            print("Goodbye!")
            break

if __name__ == '__main__':
    main()