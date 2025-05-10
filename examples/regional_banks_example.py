#!/usr/bin/env python3
"""
Example: View regional banks information
This example demonstrates how to:
1. Get regional bank information for all departments
2. Display bank details
"""

from creditagricole_particuliers import regionalbanks

def main():
    # Initialize regional banks manager
    regional_banks = regionalbanks.RegionalBanks()
    
    print("\n=== Regional Bank Information ===\n")
    
    # Test all departments from 1 to 95 (metropolitan France)
    for dept in range(1, 96):
        try:
            # Get bank information for the department
            bank_info = regional_banks.by_departement(dept)
            
            if bank_info:
                print(f"\nDepartment {dept}:")
                print(f"Bank Name: {bank_info.get('name', 'N/A')}")
                print(f"Department: {bank_info.get('department', 'N/A')}")
                print(f"URL Prefix: {bank_info.get('regionalBankUrlPrefix', 'N/A')}")
                print(f"Bank Code: {bank_info.get('code', 'N/A')}")
                print("\nContact Information:")
                print(f"Address: {bank_info.get('address', 'N/A')}")
                print(f"Phone: {bank_info.get('phone', 'N/A')}")
                print(f"Email: {bank_info.get('email', 'N/A')}")
                print("-" * 50)
        except Exception as e:
            print(f"\nDepartment {dept}: No regional bank found or error occurred")
            print(f"Error: {str(e)}")
            print("-" * 50)

if __name__ == "__main__":
    main() 