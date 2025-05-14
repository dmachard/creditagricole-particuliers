#!/usr/bin/env python3
"""
Example: View account operations
This example demonstrates how to:
1. Connect to Credit Agricole
2. Get account operations for a specific time period
3. Display operation details
"""

from datetime import datetime, timedelta
import sys
from creditagricole_particuliers import Accounts
from _utils import login, logout

def main():
    # get arguments from command line
    if len(sys.argv) < 3:
        print("Usage: account_operations_example.py <username> <department>")
        sys.exit(1)
    username = sys.argv[1]
    department = int(sys.argv[2])

    # Create session
    session = login(username, department)
    
    try:
        # Get all accounts
        accounts = Accounts(session)
        
        # Get the first account (you can modify this to select a specific account)
        account = next(iter(accounts))
        
        # Get operations for the last 30 days
        date_stop = datetime.now()
        date_start = date_stop - timedelta(days=30)
        
        print(f"\n=== Operations for Account {account.numeroCompte} ===\n")
        print(f"Period: {date_start.strftime('%Y-%m-%d')} to {date_stop.strftime('%Y-%m-%d')}\n")
        
        # Get operations
        operations = Operations(
            session=session,
            compteIdx=account.compteIdx,
            grandeFamilleCode=account.grandeFamilleCode,
            date_start=date_start.strftime("%Y-%m-%d"),
            date_stop=date_stop.strftime("%Y-%m-%d")
        )
        
        # Display operations
        for operation in operations:
            print(f"Date: {operation.dateOp}")
            print(f"Description: {operation.libelleOp}")
            print(f"Amount: {operation.montantOp}")
            print("-" * 50)
            
        # Display total number of operations
        print(f"\nTotal operations: {len(operations)}")
        
        # Example of getting operations as JSON
        operations_json = operations.as_json()
        print("\nOperations as JSON (first operation):")
        print(operations_json[0] if operations_json else "No operations found")
        
    finally:
        # Always logout when done
        logout(session)

if __name__ == "__main__":
    main() 