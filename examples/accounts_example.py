#!/usr/bin/env python3
"""
Example: List all accounts and their details
This example demonstrates how to:
1. Connect to Credit Agricole
2. List all accounts
3. Display detailed information for each account
4. Display IBAN information (currently disabled due to backend issues)
"""

import sys
from creditagricole_particuliers import Accounts
from _utils import login, logout

def main():
    # Argumente direkt aus sys.argv lesen
    if len(sys.argv) < 3:
        print("Usage: accounts_example.py <username> <department>")
        sys.exit(1)
    username = sys.argv[1]
    department = int(sys.argv[2])
    
    # Create session
    session = login(username, department)
    
    try:
        # Get all accounts
        accounts = Accounts(session)
        
        # Display account information
        print("\n=== Your Credit Agricole Accounts ===\n")
        
        for account in accounts:
            print("\nAccount Information:")
            print(f"Account Number: {account.numeroCompte}")
            
            # IBAN functionality is currently broken/not implemented in the API
            # TODO: Uncomment and implement when backend IBAN functionality is fixed
            """
            iban = account.get_iban()
            print(f"IBAN: {iban.ibanCode}")
            
            # Display detailed IBAN information
            iban_data = iban.iban
            if iban_data and 'ibanData' in iban_data:
                data = iban_data['ibanData']
                print("\nDetailed IBAN Information:")
                print(f"BIC Code: {data.get('bicCode', 'N/A')}")
                print(f"Account Holder: {data.get('titulaire', 'N/A')}")
                print(f"Bank Branch: {data.get('domiciliation', 'N/A')}")
                print(f"Bank Code: {data.get('codeBanque', 'N/A')}")
                print(f"Branch Code: {data.get('codeGuichet', 'N/A')}")
                print(f"Account Number: {data.get('numeroCompte', 'N/A')}")
                print(f"RIB Key: {data.get('cleRib', 'N/A')}")
            """
            
            print(f"Balance: {account.get_solde()}")
            print(f"Product Type: {account.account.get('libelleProduit', 'N/A')}")
            print(f"Account Type: {account.account.get('typeCompte', 'N/A')}")
            print(f"Account Status: {account.account.get('statutCompte', 'N/A')}")
            print(f"Currency: {account.account.get('devise', 'N/A')}")
            print(f"Last Balance Date: {account.account.get('dateSolde', 'N/A')}")
            if 'montantEpargne' in account.account:
                print(f"Savings Amount: {account.account['montantEpargne']}")
            print("-" * 50)
            
        # Display total balance
        print(f"\nTotal Balance: {accounts.get_solde()}")
        
        # Display balance by product type
        print("\nBalance by Product Type:")
        for product_type, balance in accounts.get_solde_per_products().items():
            print(f"{product_type}: {balance}")
            
    finally:
        # Always logout when done
        logout(session)

if __name__ == "__main__":
    main() 