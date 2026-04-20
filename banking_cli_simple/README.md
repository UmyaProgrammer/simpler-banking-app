# Simple CLI Banking App

This is a very simple command-line banking app for a school project.

## Features
- Sign up with:
  - account name
  - password
  - initial deposit
- Login with account name and password
- Deposit money
- Withdraw money with balance validation
- Check balance
- Admin portal to list all accounts and balances

## Run
```bash
python banking_cli.py
```

## Admin Login
- Username: `admin`
- Password: `admin123`

## Storage
The app stores accounts in:
```text
data/accounts.json
```

That makes it easy to replace later with a real database because the storage logic is separated into the `AccountRepository` class.

## Notes
- One username = one account
- Users cannot manage multiple accounts
- Withdrawal is blocked if the amount is greater than the current balance
