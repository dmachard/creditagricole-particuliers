#!/usr/bin/env python3
"""
Example: Comprehensive Credit Agricole API usage
This example demonstrates how to:
1. Connect to Credit Agricole using authentication credentials
2. Retrieve regional bank information for a specific department
3. List all accounts and their details including:
   - Account information and IBAN (currently disabled)
   - Recent operations within a specified date range
   - Current account balance (solde)
4. List all cards and their deferred operations
5. Properly handle session cleanup with logout

This example uses mock data by default to avoid making real API calls.
The mock data is located in the ../mocks directory relative to this script.
"""

import os
from datetime import datetime, timedelta
from creditagricole_particuliers import Accounts, Authenticator, Logout, Cards, RegionalBanks
from creditagricole_particuliers.mockconfig import MockConfig


def main():
    # Authentication credentials
    # These values are used for demonstration purposes
    username = "1234567891"  # Your Credit Agricole customer number
    password_digits = [int(d) for d in "123456"]  # Your 6-digit password
    department = 75  # Your department number (e.g., 75 for Paris)

    # Operation retrieval settings
    # These parameters control which operations to fetch
    ops_date = '2023-05-10'  # Reference date for operation retrieval
    days_of_ops = 3          # Number of days to look back from ops_date
    ops_count = 10           # Maximum number of operations to retrieve

    # Calculate the date range for operations
    # Operations will be retrieved between ops_end and ops_begin
    ops_begin = datetime.strptime(ops_date, '%Y-%m-%d').strftime('%Y-%m-%d')
    ops_end = (datetime.strptime(ops_date, '%Y-%m-%d') - timedelta(days=days_of_ops)).strftime('%Y-%m-%d')

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
        # Step 1: Get regional bank information
        print("=> Getting RegionalBank with department={department}")
        regional_bank = RegionalBanks(mock_config=mock_config).by_departement(department)
        print(f"<= RegionalBank: {regional_bank}")

        # Step 2: Authenticate and create a session
        print(f"=> Authenticating with username={username}, password={password_digits}, department={department}")
        session = Authenticator(
            username=username,
            password=password_digits,
            department=department,
            mock_config=mock_config
        )
        print("<= Session created")
        
        # Step 3: Retrieve and process all accounts
        print(f"=> Getting accounts")
        accounts = Accounts(session=session)
        print(f"<= Accounts: {len(accounts)}")
        for account in accounts:
            print(f"   * Account: {account}")

            # Note: IBAN retrieval is currently disabled
            print(f"   => Getting iban")
            iban = "currently not functional"
            #iban = account.get_iban();
            print(f"   <= Iban: {iban}")

            # Get recent operations for the account
            print(f"   => Getting operations with date_start={ops_end}, date_stop={ops_begin}, count={ops_count}")
            operations = account.get_operations(
                date_start=ops_end,
                date_stop=ops_begin,
                count=ops_count
            )
            print(f"   <= Operations: {len(operations)}")
            for operation in operations:
                print(f"      * {operation}")

            # Get current account balance
            print(f"   => Getting solde")
            solde = account.get_solde()
            print(f"   <= Solde: {solde}")

        # Step 4: Retrieve and process all cards
        print(f"=> Getting cards")
        cards = Cards(session=session)
        print(f"<= Cards: {len(cards)}")
        for card in cards:
            print(f"   * {card}")
            # Get deferred operations for each card
            print(f"   => Getting deferred operations")
            deferred_ops = card.get_operations()
            print(f"   <= DeferredOperations: {len(deferred_ops)}")
            for deferred_op in deferred_ops:
                print(f"      * {deferred_op}")
        
    finally:
        # Step 5: Always ensure proper session cleanup
        print(f"=> Logging out")
        logout = Logout(session).logout()
        print(f"<= Logged out")

if __name__ == "__main__":
    main() 