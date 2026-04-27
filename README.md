# CLI Banking App

The main goal of the app is to provide a small banking application with a CLI. Its main goal was for me to complete Code2College's Elite 102 Program and also practice my programming skills in the process. My main goal was to be able to properly connect and store data within a database using Python, and I was able to achieve that. It was a fun project to work on.

## Instructions for Setup

Simple GitHub stuff:

- Clone the repository.

### Change Admin Credentials

Change the admin username and password in `banking_cli.py`:

```python
ADMIN_USERNAME = '{Preferred Admin Login Username}'
ADMIN_PASSWORD = 'Preferred Admin Login Password'
```

### Configure Database

Put your database credentials in the `.env` file:

```env
DATA_BASE_BANK="{Your Database Name}"
DATA_BASE_PASSWORD="{Your User Password}"
```

## Database Setup

Run the following SQL commands to set up your database.

### Table 1: Users

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    balance DECIMAL(10,2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Note:**  
The initial goal was to hash the passwords so that they wouldn't be leaked if the database got hacked, but I decided that it was too much work. If you want to work with hashed passwords, go for it. The tables are created to support them, but the code currently does not.

### Table 2: Transactions

```sql
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Note:**  
I couldn't use a foreign key because it would complicate the process too much, and I didn't have enough time. I was working on a full-stack banking app, realized I couldn't finish it on time, gave up on it the day before I thought it was due, and started this mini project instead. You can, however, modify this and use foreign keys. You will need to change the code a bit, but it shouldn't be too hard since you won't need to change anything on the UI.

## Features

The app is simple, but it still has a solid foundation that you can build on.

### Admin Dashboard
- Allows you to see the users  
- Allows you to see all the transactions  

### Create User / Sign Up
- Allows you to create users with an initial deposit  

### Login
- Allows you to deposit, withdraw, and check your balance  
- The ability to see all of your transactions was not added, but you can implement that  

### Log Out
- Allows you to log out of the system to check different accounts without fully quitting the app
