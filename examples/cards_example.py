#!/usr/bin/env python3
"""
Example: View cards and their operations
This example demonstrates how to:
1. Connect to Credit Agricole
2. List all cards
3. Display card details and deferred operations
"""

import sys
from creditagricole_particuliers import Cards
from _utils import login, logout

def main():
    # Parse command line arguments
    if len(sys.argv) < 3:
        print("Usage: cards_example.py <username> <department>")
        sys.exit(1)
    username = sys.argv[1]
    department = int(sys.argv[2])
    
    # Create session
    session = login(username, department)
    
    try:
        # Get all cards
        cards = Cards(session)
        
        print("\n=== Your Credit Agricole Cards ===\n")
        
        # Display all cards
        for card in cards:
            print("\nCard Information:")
            print(f"Card Type: {card.typeCarte}")
            print(f"Card Holder: {card.titulaire}")
            print(f"Card ID: {card.idCarte}")
            print(f"Associated Account ID: {card.idCompte}")
            print("-" * 50)
            
            # Get and display deferred operations for this card
            print("\nDeferred Operations:")
            deferred_ops = card.get_operations()
            for op in deferred_ops:
                print(f"Date: {op.dateOp}")
                print(f"Description: {op.libelleOp}")
                print(f"Amount: {op.montantOp}")
                print("-" * 30)
        
        # Example of searching for a specific card
        print("\n=== Search for a Specific Card ===\n")
        # Get the first card's last 4 digits for the search example
        first_card = next(iter(cards), None)
        if first_card:
            last_four_digits = first_card.idCarte[-4:]
            print(f"Searching for card ending with: {last_four_digits}")
            specific_card = cards.search(last_four_digits)
            if specific_card:
                print(f"Found card: {specific_card.typeCarte} ({specific_card.titulaire})")
            else:
                print("Card not found")
        else:
            print("No cards found to search")
            
    finally:
        # Always logout when done
        logout(session)

if __name__ == "__main__":
    main() 