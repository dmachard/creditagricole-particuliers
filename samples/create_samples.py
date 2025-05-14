#!/usr/bin/env python3
"""
Ce script se connecte à Crédit Agricole et extrait des structures de réponse pour comprendre
le schéma complet des objets renvoyés par l'API.
Crée des fichiers séparés pour chaque compte, carte, etc.

Deux modes disponibles:
- 'data': sauvegarde les données réelles (sensibles) sans suffixe
- 'types': sauvegarde uniquement la structure avec des valeurs fictives avec le suffixe '_types'
"""

import json
import os
import sys
import argparse
import re
from datetime import datetime, timedelta
from getpass import getpass
from typing import Any, Dict, List, Union

from creditagricole_particuliers import (
    authenticator, accounts, regionalbanks, cards
)

def save_json(data, filename, target_dir):
    """Save data to a JSON file"""
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, filename), 'w') as f:
        json.dump(data, f, indent=2)

def convert_to_type_structure(data: Any) -> Any:
    """
    Convertit des données réelles en structure de types.
    Remplace les valeurs par des placeholders selon leur type.
    """
    if isinstance(data, str):
        # Remplacer les chaînes par une chaîne vide au lieu de "str"
        return ""
    elif isinstance(data, int):
        return 0
    elif isinstance(data, float):
        return 0.0
    elif isinstance(data, bool):
        return False
    elif isinstance(data, list):
        if data:
            # Ne prend que le premier élément comme exemple
            return [convert_to_type_structure(data[0])]
        return []
    elif isinstance(data, dict):
        return {k: convert_to_type_structure(v) for k, v in data.items()}
    elif data is None:
        return None
    else:
        # Pour les types non gérés
        return f"type:{type(data).__name__}"

def create_placeholder(original_id: str) -> str:
    """
    Crée un placeholder pour un identifiant en remplaçant tous les caractères par des '0'.
    Utilisé pour générer des noms de fichiers sans données sensibles.
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
                       help="Mode de génération: 'data' pour données réelles (défaut), 'types' pour structure avec placeholders")
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

    try:
        # Authenticate
        print("Authenticating...")
        auth = authenticator.Authenticator(
            username=args.username,
            password=password_digits,
            department=args.department
        )
        
        # Get regional banks information
        print("Getting regional banks...")
        rb = regionalbanks.RegionalBanks()
        
        # Get specific regional bank for the user's department
        print(f"Getting regional bank information for department {args.department}...")
        bank = rb.by_departement(int(args.department))
        
        # Apply type structure if needed
        if args.mode == 'types':
            # Utilisez toujours le département original pour le nom de fichier même en mode types
            dept_placeholder = create_placeholder(str(args.department))
            bank = convert_to_type_structure(bank)
            # Save with types suffix
            save_json(bank, f"regionalBank_{dept_placeholder}_types.json", target_dir)
        else:
            # Save without sample suffix in data mode
            save_json(bank, f"regionalBank_{args.department}.json", target_dir)
        
        # Get accounts
        print("Getting accounts...")
        accs = accounts.Accounts(auth)
        accs_data = json.loads(accs.as_json())
        
        # Apply type structure if needed
        if args.mode == 'types':
            # Keep only one account as an example
            if accs_data:
                # Récupérer le numéro de compte pour créer un placeholder pour le nom de fichier
                real_account_number = accs_data[0]['numeroCompte']
                account_placeholder = create_placeholder(real_account_number)
                
                # Convertir en structure de types
                accs_data = [convert_to_type_structure(accs_data[0])]
                
                save_json(accs_data, 'accounts_types.json', target_dir)
                
                # Process only the first account
                account = accs_data[0]
                print(f"Processing sample account structure...")
                
                # Save individual account data with types suffix, using placeholder in filename
                save_json(account, f"account_{account_placeholder}_types.json", target_dir)
                
                # Get operations for this account (use a real account number for API call)
                print(f"Getting operations sample structure...")
                acc = accs.search(real_account_number)
                current_date = datetime.today()
                previous_date = current_date - timedelta(days=30)
                date_stop = current_date.strftime('%Y-%m-%d')
                date_start = previous_date.strftime('%Y-%m-%d')
                
                try:
                    ops = acc.get_operations(date_start=date_start, date_stop=date_stop, count=10)
                    ops_data = json.loads(ops.as_json())
                    if ops_data:
                        # Keep only one operation
                        ops_data = [convert_to_type_structure(ops_data[0])]
                    save_json(ops_data, f"account_{account_placeholder}_operations_types.json", target_dir)
                except Exception as e:
                    print(f"Error getting operations sample: {e}")
        else:
            # Original behavior - save all real accounts data without sample suffix
            save_json(accs_data, 'accounts.json', target_dir)
            
            # Process each account individually
            for account in accs_data:
                account_number = account['numeroCompte']
                print(f"Processing account {account_number}...")
                
                # Save individual account data
                save_json(account, f"account_{account_number}.json", target_dir)
                
                # Get operations for this account
                print(f"Getting operations for account {account_number}...")
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
            
        # Get cards
        print("Getting cards...")
        try:
            user_cards = cards.Cards(auth)
            cards_data = json.loads(user_cards.as_json())
            
            # Apply type structure if needed
            if args.mode == 'types':
                if cards_data:
                    # Récupérer l'ID de la carte pour créer un placeholder pour le nom de fichier
                    real_card_id = cards_data[0]['idCarte']
                    real_card_last_4 = real_card_id[-4:]
                    card_last_4_placeholder = create_placeholder(real_card_last_4)
                    
                    # Convertir en structure de types
                    cards_data = [convert_to_type_structure(cards_data[0])]
                    
                    save_json(cards_data, 'cards_types.json', target_dir)
                    
                    # Process only the first card
                    card = cards_data[0]
                    print(f"Processing sample card structure...")
                    
                    # Save individual card data with types suffix, using placeholder in filename
                    save_json(card, f"card_{card_last_4_placeholder}_types.json", target_dir)
                    
                    # Get operations for a card (use real card for API call)
                    try:
                        print(f"Getting card operations sample structure...")
                        card_obj = user_cards.search(real_card_last_4)
                        deferred_ops = card_obj.get_operations()
                        ops_data = json.loads(deferred_ops.as_json())
                        if ops_data:
                            # Keep only one operation
                            ops_data = [convert_to_type_structure(ops_data[0])]
                        save_json(ops_data, f"card_{card_last_4_placeholder}_operations_types.json", target_dir)
                    except Exception as e:
                        print(f"Error getting card operations sample: {e}")
            else:
                # Original behavior - save all real cards data without sample suffix
                save_json(cards_data, 'cards.json', target_dir)
                
                # Process each card individually
                for card in cards_data:
                    card_id = card['idCarte']
                    card_last_4 = card_id[-4:]
                    print(f"Processing card ending with {card_last_4}...")
                    
                    # Save individual card data
                    save_json(card, f"card_{card_last_4}.json", target_dir)
                    
                    # Get operations for this card
                    try:
                        print(f"Getting operations for card {card_last_4}...")
                        card_obj = user_cards.search(card_last_4)
                        deferred_ops = card_obj.get_operations()
                        ops_data = json.loads(deferred_ops.as_json())
                        save_json(ops_data, f"card_{card_last_4}_operations.json", target_dir)
                    except Exception as e:
                        print(f"Error getting operations for card {card_last_4}: {e}")
                    
        except Exception as e:
            print(f"Error getting cards: {e}")
            
        print("Done!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 