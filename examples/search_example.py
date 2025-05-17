#!/usr/bin/env python3
"""
Example: Search for specific account and card
This example demonstrates how to:
1. Connect to Credit Agricole using authentication credentials
2. Search for a specific account by its account number
3. Search for a specific card by its last 4 digits
4. Display account and card details
5. Properly handle session cleanup with logout

This example uses mock data by default to avoid making real API calls.
The mock data is located in the ../mocks directory relative to this script.
"""

import os
from creditagricole_particuliers import Accounts, Authenticator, Logout, Cards
from creditagricole_particuliers.mockconfig import MockConfig


def main():
    # Authentication credentials
    # These values are used for demonstration purposes
    username = "1234567891"  # Your Credit Agricole customer number
    password_digits = [int(d) for d in "123456"]  # Your 6-digit password
    department = 75  # Your department number (e.g., 75 for Paris)

    # Search parameters
    # These values should match the mock data in the mocks directory
    account_number = "12345678901"  # Account number to search for (from accounts-1_mock.json)
    card_last_digits = "1098"       # Last 4 digits of the card to search for (from cards_mock.json)

    # Configure mock data settings
    # This setup allows using mock data instead of making real API calls
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mocks_dir = os.path.abspath(os.path.join(script_dir, '..', 'mocks'))
    
    mock_config = MockConfig(
        useMocksDir=mocks_dir,      # Directory containing mock data files
        writeMocksDir=None,         # No writing of mock data
        useMockSuffix="mock",       # Suffix for mock data files
        writeMockSuffix="mock"      # Suffix for written mock data files
    )
    print(f"# {mock_config}")

    try:
        # Step 1: Authenticate and create a session
        print(f"=> Authenticating with username={username}, password={password_digits}, department={department}")
        session = Authenticator(
            username=username,
            password=password_digits,
            department=department,
            mock_config=mock_config
        )
        print("<= Session created")
        
        # Step 2: Search for a specific account
        print(f"=> Searching for account with number={account_number}")
        account = Accounts(session=session).search(account_number)
        print(f"<= Found account: {account}")

        # Step 3: Search for a specific card
        print(f"=> Searching for card with last digits={card_last_digits}")
        card = Cards(session=session).search(card_last_digits)
        print(f"<= Found card: {card}")
        
    finally:
        # Step 4: Always ensure proper session cleanup
        print(f"=> Logging out")
        logout = Logout(session).logout()
        print(f"<= Logged out")

if __name__ == "__main__":
    main() 