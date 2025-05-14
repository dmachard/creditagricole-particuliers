#!/usr/bin/env python3
"""
Common utilities for Credit Agricole examples
"""

from getpass import getpass
from creditagricole_particuliers import Authenticator, Logout

def login(username, department):
    # Get password securely
    password = getpass('Enter your Credit Agricole password (digits only): ')
    # Convert password string to list of integers
    password_digits = [int(d) for d in password]
    return Authenticator(username, password_digits, department)

def logout(session):
    Logout(session) 