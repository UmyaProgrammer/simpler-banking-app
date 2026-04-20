from db import get_bank_db
from datetime import datetime

# This function creates a new user and stores them in the database
def create_user(name, password, balance):
    # Open a connection to the database
    db = get_bank_db()
    cursor = db.cursor()

    # Capture the exact time the user is created
    created_at = datetime.now()

    # SQL query to insert a new user into the users table
    query = """
        INSERT INTO users (name, password_hash, balance, created_at)
        VALUES (%s, %s, %s, %s)
    """

    # Values that will be inserted into the query
    values = (name, password, balance, created_at)

    # Execute the query with the provided values
    cursor.execute(query, values)

    # Save the changes to the database
    db.commit()

    # Clean up: close cursor and database connection
    cursor.close()
    db.close()

    print("User created successfully!")


# This function retrieves a single user based on their username
def get_user(username:str):
    # Connect to the database
    conn = get_bank_db()
    # dictionary=True lets us access columns by name instead of index
    cursor = conn.cursor(dictionary=True)

    # Fetch the user with the given username
    cursor.execute("SELECT * FROM users WHERE name = %s", (username,))
    user = cursor.fetchone()

    # Close everything after we're done
    cursor.close()
    conn.close()

    # Return the user data (or None if not found)
    return user


# This function deposits money into a user's account
def user_deposit(username:str, amount:float):
    db = get_bank_db()
    cursor = db.cursor()

    # Increase the user's balance by the given amount
    query = "UPDATE users SET balance = balance + %s WHERE name = %s"
    cursor.execute(query, (amount, username))

    # Commit the update so it actually saves
    db.commit()

    # Fetch the updated balance so we can return it
    cursor.execute("SELECT balance FROM users WHERE name = %s", (username,))
    new_balance = cursor.fetchone()[0]

    # Close connections
    cursor.close()
    db.close()

    return new_balance


# This function withdraws money from a user's account
def user_withdraw(username:str, amount:float):
    db = get_bank_db()
    cursor = db.cursor()

    # Decrease the user's balance by the given amount
    query = "UPDATE users SET balance = balance - %s WHERE name = %s"
    cursor.execute(query, (amount, username))

    # Save the changes
    db.commit()

    # Get the updated balance after withdrawal
    cursor.execute("SELECT balance FROM users WHERE name = %s", (username,))
    new_balance = cursor.fetchone()[0]

    # Close everything properly
    cursor.close()
    db.close()

    return new_balance


# Simple helper function to just get a user's balance
def user_get_balance(username:str)->float:
    return get_user(username)['balance']


# This is an admin function that returns all users in the database
def admin_get_users()->list:
    conn = get_bank_db()
    cursor = conn.cursor(dictionary=True)

    # Get every user from the users table
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    # Close connections
    cursor.close()
    conn.close()

    return users


def get_all_transactions()->list:
    conn = get_bank_db()
    cursor = conn.cursor(dictionary=True)

    # Get every user from the users table
    cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()

    # Close connections
    cursor.close()
    conn.close()

    return transactions


# This function creates a new user and stores them in the database
def create_transaction(user_id:str, type_of_action:str, amount:float):
     # Open a connection to the database
    db = get_bank_db()
    cursor = db.cursor()

    # Capture the exact time the user is created
    created_at = datetime.now()

    # SQL query to insert a new user into the users table
    query = """
        INSERT INTO transactions (user_id, type, amount, created_at)
        VALUES (%s, %s, %s, %s)
    """

    # Values that will be inserted into the query
    values = (user_id, type_of_action, amount, created_at)

    # Execute the query with the provided values
    cursor.execute(query, values)

    # Save the changes to the database
    db.commit()

    # Clean up: close cursor and database connection
    cursor.close()
    db.close()


# This block only runs if you execute this file directly
if __name__ == "__main__":
    # Example test: deposit 200 into "someone"'s account
    print(get_user("someone"))