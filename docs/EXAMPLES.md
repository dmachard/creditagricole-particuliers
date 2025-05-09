# Credit Agricole Python Library Examples

This document provides practical examples of how to use the Credit Agricole Python library. These examples cover all core components and common use cases.

## Table of Contents

1. [Authentication](#authentication)
2. [Account Management](#account-management)
3. [Operations](#operations)
4. [Cards Management](#cards-management)

## Authentication

### Basic Authentication

```python
from creditagricole_particuliers import Authenticator, Logout

# Initialize the authenticator with your credentials
# Password must be a list of integers representing the digits
auth = Authenticator(
    username="your_username",
    password=[1, 2, 3, 4, 5, 6],  # Example: 123456
    department=75  # Paris department code
)

try:
    # Perform authentication
    auth.authenticate()
    
    # ... perform operations ...
    
finally:
    # Always logout when done
    Logout(auth)
```

## Account Management

### Listing All Accounts

```python
from creditagricole_particuliers import Authenticator, Accounts, Logout

# Initialize and authenticate
auth = Authenticator(
    username="your_username",
    password=[1, 2, 3, 4, 5, 6],  # Example: 123456
    department=75
)

try:
    auth.authenticate()

    # Get all accounts
    accounts = Accounts(auth)

    # Print account details
    for account in accounts:
        print(f"Account Number: {account.numeroCompte}")
        print(f"Balance: {account.get_solde()}")
        print(f"Product Type: {account.account.get('libelleProduit', 'N/A')}")
        print(f"Account Type: {account.account.get('typeCompte', 'N/A')}")
        print(f"Account Status: {account.account.get('statutCompte', 'N/A')}")
        print(f"Currency: {account.account.get('devise', 'N/A')}")
        print(f"Last Balance Date: {account.account.get('dateSolde', 'N/A')}")
        if 'montantEpargne' in account.account:
            print(f"Savings Amount: {account.account['montantEpargne']}")
        print("---")

    # Get total balance
    total_balance = accounts.get_solde()
    print(f"Total balance: {total_balance}")

    # Get balance by product type
    balances_by_product = accounts.get_solde_per_products()
    print("Balances by product:", balances_by_product)

finally:
    # Always logout when done
    Logout(auth)
```

## Operations

### Getting Account Operations

```python
from creditagricole_particuliers import Authenticator, Accounts, Operations, Logout
from datetime import datetime, timedelta

auth = Authenticator(
    username="your_username",
    password=[1, 2, 3, 4, 5, 6],  # Example: 123456
    department=75
)

try:
    auth.authenticate()

    # Get first account
    accounts = Accounts(auth)
    account = next(iter(accounts))

    # Get operations for the last 30 days
    date_stop = datetime.now()
    date_start = date_stop - timedelta(days=30)

    operations = Operations(
        session=auth,
        compteIdx=account.compteIdx,
        grandeFamilleCode=account.grandeFamilleCode,
        date_start=date_start.strftime("%Y-%m-%d"),
        date_stop=date_stop.strftime("%Y-%m-%d")
    )

    # Print operations
    for operation in operations:
        print(f"Date: {operation.dateOp}")
        print(f"Description: {operation.libelleOp}")
        print(f"Amount: {operation.montantOp}")
        print("---")

    # Get operations as JSON
    operations_json = operations.as_json()

finally:
    # Always logout when done
    Logout(auth)
```

## Cards Management

### Listing All Cards

```python
from creditagricole_particuliers import Authenticator, Cards, Logout

auth = Authenticator(
    username="your_username",
    password=[1, 2, 3, 4, 5, 6],  # Example: 123456
    department=75
)

try:
    auth.authenticate()

    # Get all cards
    cards = Cards(auth)

    # Print card details
    for card in cards:
        print(f"Card Type: {card.typeCarte}")
        print(f"Card Holder: {card.titulaire}")
        print(f"Card ID: {card.idCarte}")
        print(f"Associated Account ID: {card.idCompte}")
        print("---")

    # Search for a specific card
    last_four_digits = "1234"  # Example: last 4 digits of card number
    specific_card = cards.search(last_four_digits)
    if specific_card:
        print(f"Found card: {specific_card.typeCarte} ({specific_card.titulaire})")

finally:
    # Always logout when done
    Logout(auth)
```

### Getting Card Operations

```python
from creditagricole_particuliers import Authenticator, Cards, Logout

auth = Authenticator(
    username="your_username",
    password=[1, 2, 3, 4, 5, 6],  # Example: 123456
    department=75
)

try:
    auth.authenticate()

    cards = Cards(auth)

    # Get first card
    card = next(iter(cards))

    # Get deferred operations for the card
    deferred_ops = card.get_operations()

    # Print deferred operations
    for operation in deferred_ops:
        print(f"Date: {operation.dateOp}")
        print(f"Description: {operation.libelleOp}")
        print(f"Amount: {operation.montantOp}")
        print("---")

finally:
    # Always logout when done
    Logout(auth)
```

Remember to replace `your_username`, `your_password` (as a list of integers), and the department code (e.g., 75 for Paris) with your actual credentials. 