#!/usr/bin/env python3
"""
Common utilities for Credit Agricole examples
"""

import argparse
from creditagricole_particuliers import Authenticator, Logout

def parse_args():
    parser = argparse.ArgumentParser(description='Credit Agricole Example')
    parser.add_argument('--username', required=True, help='Your Credit Agricole username')
    parser.add_argument('--password', required=True, help='Your Credit Agricole password (6 digits)')
    parser.add_argument('--department', required=True, type=int, help='Your department code')
    return parser.parse_args()

def login(username, password, department):
    # Convert password string to list of integers
    password_digits = [int(d) for d in password]
    return Authenticator(username, password_digits, department)

def logout(session):
    Logout(session) 