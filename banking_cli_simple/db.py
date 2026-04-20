import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables from the .env file into the system
# This lets us keep sensitive info (like passwords) out of our code
load_dotenv()

# This function creates and returns a connection to the bank database
def get_bank_db() -> mysql.connector.connect:
    return mysql.connector.connect(
        host="localhost",  # The database is running on this same machine
        user="root",       # Default MySQL user (you might change this later for security)
        
        # Pull the database password from environment variables instead of hardcoding it
        password=os.getenv("DATA_BASE_PASSWORD"),
        
        # Also grab the database name from the environment
        database=os.getenv("DATA_BASE_BANK")
    )

