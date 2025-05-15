#!/usr/bin/env python3
"""
This script connects to Crédit Agricole and extracts response structures to understand
the complete schema of objects returned by the API.
Creates separate files for each account, card, etc.

Two available modes:
- 'data': saves real data (sensitive) without suffix
- 'types': saves only the structure with dummy values with the '_types' suffix

Mock functionality:
- Use --mocks-dir to specify mock directory
- Use --write-mocks to write API responses to mock files
- Use --use-mocks to use mock data instead of API calls
"""

import json
import os
import sys
import argparse
import re
from datetime import datetime, timedelta
from getpass import getpass
from typing import Any, Dict, List, Union
from collections import defaultdict

from creditagricole_particuliers import (
    authenticator, accounts, regionalbanks, cards, logout, MockConfig
)

def save_json(data, filename, target_dir):
    """Save data to a JSON file"""
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)

def convert_to_type_structure(data: Any) -> Any:
    """
    Converts real data to type structure.
    Replaces values with placeholders according to their type.
    """
    if isinstance(data, str):
        # Replace strings with empty string instead of "str"
        return ""
    elif isinstance(data, int):
        return 0
    elif isinstance(data, float):
        return 0.0
    elif isinstance(data, bool):
        return False
    elif isinstance(data, list):
        if data:
            # Only take the first element as an example
            return [convert_to_type_structure(data[0])]
        return []
    elif isinstance(data, dict):
        return {k: convert_to_type_structure(v) for k, v in data.items()}
    elif data is None:
        return None
    else:
        # For unhandled types
        return f"type:{type(data).__name__}"

def create_placeholder(original_id: str) -> str:
    """
    Creates a placeholder for an identifier by replacing all characters with '0'.
    Used to generate filenames without sensitive data.
    """
    if re.match(r'^[0-9]+$', original_id):
        return '0' * len(original_id)
    return 'placeholder'

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Extract Credit Agricole API schemas')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', help='Password (digits only). If not provided, will be prompted securely')
    parser.add_argument('--department', required=True, type=int, help='Department code')
    parser.add_argument('--output-dir', default=None, help='Output directory for samples')
    parser.add_argument('--mode', choices=['data', 'types'], default='data',
                       help="Generation mode: 'data' for real data (default), 'types' for structure with placeholders")
    
    # Add mock functionality arguments
    parser.add_argument('--use-mocks-dir', default=None, help='Directory for mock files to use')
    parser.add_argument('--write-mocks-dir', default=None, help='Directory for mock files to write')
    parser.add_argument('--use-mock-suffix', default='mock', help='Suffix for mock files to use')
    parser.add_argument('--write-mock-suffix', default='mock', help='Suffix for mock files to write')
    
    args = parser.parse_args()

    # Get password either from argument or prompt
    password = args.password
    if not password:
        password = getpass('Enter your password (digits only): ')

    # Convert password string to digits array
    password_digits = [int(d) for d in password]
    
    # Set default output directory based on mode if none provided
    if args.output_dir is None:
        if args.mode == 'data':
            target_dir = './data'
        else:  # types mode
            target_dir = './types'
    else:
        target_dir = args.output_dir
    
    # Ensure output directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Create MockConfig object if mock functionality is enabled
    mock_config = None
    if args.use_mocks_dir or args.write_mocks_dir:
        mock_config = MockConfig(
            useMocksDir=args.use_mocks_dir,
            writeMocksDir=args.write_mocks_dir,
            useMockSuffix=args.use_mock_suffix,
            writeMockSuffix=args.write_mock_suffix
        )
        print(mock_config)

    try:
        # Authenticate
        print("Authenticating...")
        auth = authenticator.Authenticator(
            username=args.username,
            password=password_digits,
            department=args.department,
            mock_config=mock_config
        )
        
        # Get regional banks information
        print("Getting regional banks...")
        rb = regionalbanks.RegionalBanks(mock_config=mock_config)
        
        # Get specific regional bank for the user's department
        print(f"Getting regional bank information for department {args.department}...")
        bank = rb.by_departement(int(args.department))
        # Apply type structure if needed
        if args.mode == 'types':
            bank = convert_to_type_structure(bank)
            # Save with types suffix, no placeholder
            save_json(bank, "regionalBank_types.json", target_dir)
        else:
            # Save without sample suffix in data mode
            save_json(bank, f"regionalBank_{args.department}.json", target_dir)
        
        # Get accounts
        print("Getting accounts...")
        accs = accounts.Accounts(auth)
        accs_data = json.loads(accs.as_json())
        
        # Apply type structure if needed
        if args.mode == 'types':
            if accs_data:
                # Take only one example and convert to type structure
                first_account = convert_to_type_structure(accs_data[0])
                
                # Save the first account as a global example
                save_json(first_account, 'account_types.json', target_dir)
                
                # Get operations for the first account
                real_account_number = accs_data[0]['numeroCompte']
                
                print(f"Retrieving operations for example account...")
                acc = accs.search(real_account_number)
                current_date = datetime.today()
                previous_date = current_date - timedelta(days=30)
                date_stop = current_date.strftime('%Y-%m-%d')
                date_start = previous_date.strftime('%Y-%m-%d')
                
                try:
                    ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                    ops_data = json.loads(ops.as_json())
                    if ops_data:
                        # Save a global operation example
                        operation_example = convert_to_type_structure(ops_data[0])
                        save_json(operation_example, "operation_types.json", target_dir)
                except Exception as e:
                    print(f"Error retrieving operations: {e}")
        else:
            # Group accounts by grandeFamilleProduitCode
            accounts_by_code = defaultdict(list)
            for account in accs_data:
                code = account.get('grandeFamilleProduitCode', 'unknown')
                accounts_by_code[code].append(account)
            
            # Save all accounts into a single file
            save_json(accs_data, "accounts.json", target_dir)
            
            # Process each account for operations and IBAN
            for account in accs_data:
                account_number = account['numeroCompte']
                print(f"Getting operations for account {account_number}...")
                
                # Get operations for this account
                acc = accs.search(account_number)
                current_date = datetime.today()
                previous_date = current_date - timedelta(days=30)
                date_stop = current_date.strftime('%Y-%m-%d')
                date_start = previous_date.strftime('%Y-%m-%d')
                
                try:
                    ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                    ops_data = json.loads(ops.as_json())
                    save_json(ops_data, f"account_{account_number}_operations.json", target_dir)
                except Exception as e:
                    print(f"Error getting operations for account {account_number}: {e}")
                
                # Get IBAN for this account (empty object if not available)
                print(f"Getting IBAN for account {account_number}...")
                try:
                    # We're just creating an empty object for IBAN as seen in the sample
                    # You might need to implement the actual IBAN retrieval if needed
                    save_json({}, f"account_{account_number}_iban.json", target_dir)
                except Exception as e:
                    print(f"Error getting IBAN for account {account_number}: {e}")
            
        # Get cards
        print("Getting cards...")
        try:
            user_cards = cards.Cards(auth)
            cards_data = json.loads(user_cards.as_json())
            
            # Apply type structure if needed
            if args.mode == 'types':
                if cards_data:
                    # Get the card ID for the API call
                    real_card_id = cards_data[0]['idCarte']
                    real_card_last_4 = real_card_id[-4:]
                    
                    # Convert to type structure
                    card_example = convert_to_type_structure(cards_data[0])
                    
                    # Save a single card example
                    save_json(card_example, 'card_types.json', target_dir)
                    
                    # Get operations for a card (use real card for API call)
                    try:
                        print(f"Getting card operations sample structure...")
                        card_obj = user_cards.search(real_card_last_4)
                        deferred_ops = card_obj.get_operations()
                        ops_data = json.loads(deferred_ops.as_json())
                        if ops_data:
                            # Keep only one operation
                            operation_example = convert_to_type_structure(ops_data[0])
                            save_json(operation_example, "operation_card_types.json", target_dir)
                    except Exception as e:
                        print(f"Error getting card operations sample: {e}")
            else:                
                # Save all cards data with new filename format
                new_cards_filename = f"cards.json"
                save_json(cards_data, new_cards_filename, target_dir)
                
                # Process each card individually for operations
                for i, card in enumerate(cards_data):
                    card_id = card['idCarte']
                    card_last_4 = card_id.split()[-1][-4:] if ' ' in card_id else card_id[-4:]
                    print(f"Processing card ending with {card_last_4}...")
                    
                    # Get operations for this card
                    try:
                        print(f"Getting operations for card {card_last_4}...")
                        card_obj = user_cards.search(card_last_4)
                        deferred_ops = card_obj.get_operations()
                        ops_data = json.loads(deferred_ops.as_json())
                        new_operations_filename = f"card_{card_last_4}_operations.json"
                        save_json(ops_data, new_operations_filename, target_dir)
                    except Exception as e:
                        print(f"Error getting operations for card {card_last_4}: {e}")
            
        except Exception as e:
            print(f"Error getting cards: {e}")
        
        # Logout properly
        print("Logging out...")
        try:
            logout_handler = logout.Logout(auth)
            logout_handler.logout()
            print("Successfully logged out")
        except Exception as e:
            print(f"Error during logout: {e}")
            
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 