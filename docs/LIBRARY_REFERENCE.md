# Credit Agricole Python Library Documentation

Technical reference for the [creditagricole-particuliers](https://github.com/coolcow/creditagricole-particuliers) Python library.

## Table of Contents

1. [Overview](#overview)
2. [Core Components](#core-components)
   - [Authentication](#authentication)
   - [Account Management](#account-management)
   - [Operations](#operations)
   - [Cards Management](#cards-management)
   - [IBAN Management](#iban-management)
   - [Session Management](#session-management)
   - [Regional Banks](#regional-banks)
3. [Data Structures](#data-structures)
   - [Constants](#constants)
   - [Object Structures](#object-structures)

## Overview

This library provides a Python interface to Credit Agricole's online banking services. It implements a client-side API that interacts with Credit Agricole's web interface to provide programmatic access to banking operations.

## Core Components

### Authentication

#### `Authenticator` Class
**File**: `authenticator.py`

Handles user authentication and session management.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `url` | `str` | Base URL for Credit Agricole website |
| `ssl_verify` | `bool` | SSL verification flag |
| `username` | `str` | User's login username |
| `password` | `list[int]` | User's login password as array of digits |
| `department` | `int` | User's department code |
| `regional_bank_url` | `str` | Regional bank URL prefix |
| `cookies` | `dict` | Session cookies |
| `keypadId` | `str` | Keypad ID for secure authentication |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `username: str`<br>`password: list[int]`<br>`department: int` | - | Initializes authenticator and performs authentication |
| `find_regional_bank` | `use_local: bool = True` | - | Finds regional bank URL, uses local aliases.json if use_local is True |
| `map_digit` | `key_layout: list[str]`<br>`digit: str` | `int` | Maps digits to keypad layout |
| `authenticate` | - | - | Performs authentication process |

### Account Management

#### `Account` Class
**File**: `accounts.py`

Represents a single bank account.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `account` | `dict` | Account details |
| `numeroCompte` | `str` | Account number |
| `compteIdx` | `str` | Account index |
| `grandeFamilleCode` | `str` | Product family code |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator`<br>`account: dict` | - | Initializes account with session and details |
| `__str__` | - | `str` | String representation of the account |
| `get_iban` | - | `Iban` | Returns IBAN information |
| `get_operations` | `date_start: str = None`<br>`date_stop: str = None`<br>`count: int = 100`<br>`sleep: int \| None = None` | `Operations` | Retrieves account operations |
| `as_json` | - | `str` | Returns account details as JSON |
| `get_solde` | - | `float` | Returns account balance (montantEpargne if available, otherwise solde) |

#### `Accounts` Class
**File**: `accounts.py`

Manages multiple bank accounts.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `accounts_list` | `list[Account]` | List of Account objects |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator` | - | Initializes accounts manager and automatically calls get_accounts_per_products() |
| `__iter__` | - | `Iterator[Account]` | Iterator implementation |
| `__next__` | - | `Account` | Next item in iteration |
| `search` | `num: str` | `Account` | Searches for account by number |
| `as_json` | - | `str` | Returns all accounts as JSON |
| `get_accounts_per_products` | - | - | Retrieves accounts grouped by product type and populates accounts_list |
| `get_solde` | - | `float` | Returns total balance across all accounts |
| `get_solde_per_products` | - | `dict[str, float]` | Returns balances grouped by product type |

### Operations

#### `Operation` Class
**File**: `operations.py`

Represents a single bank operation/transaction.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `descr` | `dict` | Complete operation details |
| `libelleOp` | `str` | Operation description |
| `dateOp` | `str` | Operation date |
| `montantOp` | `float` | Operation amount |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `descr: dict` | - | Initializes operation with details |
| `__str__` | - | `str` | String representation of the operation |
| `as_json` | - | `str` | Returns operation details as JSON |

#### `Operations` Class
**File**: `operations.py`

Manages bank operations/transactions.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `compteIdx` | `str` | Account index |
| `grandeFamilleCode` | `str` | Product family code |
| `date_start` | `str` | Start date for operations |
| `date_stop` | `str` | End date for operations |
| `list_operations` | `list[Operation]` | List of Operation objects |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator`<br>`compteIdx: str`<br>`grandeFamilleCode: str`<br>`date_start: str`<br>`date_stop: str`<br>`count: int = 100`<br>`sleep: int \| None = None` | - | Initializes operations manager |
| `__iter__` | - | `Iterator[Operation]` | Iterator implementation |
| `__next__` | - | `Operation` | Next item in iteration |
| `as_json` | - | `str` | Returns all operations as JSON |
| `get_operations` | `count: int`<br>`startIndex: str \| None = None`<br>`limit: int = 30`<br>`sleep: int \| None = None` | - | Retrieves operations within date range and populates list_operations. Uses pagination with limit parameter to control batch size. Sleep parameter allows rate limiting between requests. |

#### `DeferredOperations` Class
**File**: `operations.py`

Manages deferred card operations.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `compteIdx` | `str` | Account index |
| `grandeFamilleCode` | `str` | Product family code |
| `carteIdx` | `str` | Card index |
| `list_operations` | `list[Operation]` | List of Operation objects |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator`<br>`compteIdx: str`<br>`grandeFamilleCode: str`<br>`carteIdx: str` | - | Initializes deferred operations manager |
| `__iter__` | - | `Iterator[Operation]` | Iterator implementation |
| `__next__` | - | `Operation` | Next item in iteration |
| `as_json` | - | `str` | Returns all deferred operations as JSON |
| `get_operations` | - | - | Retrieves deferred operations and populates list_operations |

### Cards Management

#### `Card` Class
**File**: `cards.py`

Represents a single bank card.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `card` | `dict` | Card details |
| `idCompte` | `str` | Associated account ID |
| `typeCarte` | `str` | Card type |
| `idCarte` | `str` | Card ID |
| `titulaire` | `str` | Card holder name |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator`<br>`card: dict` | - | Initializes card with session and details |
| `__str__` | - | `str` | String representation of the card |
| `get_operations` | - | `DeferredOperations` | Retrieves deferred operations for the card |
| `as_json` | - | `str` | Returns card details as JSON |

#### `Cards` Class
**File**: `cards.py`

Manages multiple bank cards.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `cards_list` | `list[Card]` | List of Card objects |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator` | - | Initializes cards manager |
| `__iter__` | - | `Iterator[Card]` | Iterator implementation |
| `__next__` | - | `Card` | Next item in iteration |
| `as_json` | - | `str` | Returns all cards as JSON |
| `search` | `num_last_digits: str` | `Card` | Searches for card by last digits |
| `get_cards_per_account` | - | - | Retrieves cards grouped by account and populates cards_list |

### IBAN Management

#### `Iban` Class
**File**: `iban.py`

Manages IBAN information for an account.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `session` | `Authenticator` | Authentication session |
| `compteIdx` | `str` | Account index |
| `numeroCompte` | `str` | Account number |
| `grandeFamilleCode` | `str` | Product family code |
| `iban` | `dict` | Complete IBAN details |
| `ibanCode` | `str` | IBAN code |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator`<br>`compteIdx: str`<br>`grandeFamilleCode: str`<br>`numeroCompte: str` | - | Initializes IBAN manager |
| `__str__` | - | `str` | String representation of the IBAN |
| `get_iban_data` | - | - | Retrieves IBAN information from the API and populates iban and ibanCode |
| `as_json` | - | `str` | Returns IBAN details as JSON |

### Session Management

#### `Logout` Class
**File**: `logout.py`

Handles user logout from the banking service.

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | `session: Authenticator` | - | Initializes logout handler and performs logout |
| `logout` | - | - | Performs the logout process |

### Regional Banks

#### `RegionalBanks` Class
**File**: `regionalbanks.py`

Manages regional bank information.

##### Properties
| Property | Type | Description |
|----------|------|-------------|
| `url` | `str` | Base URL for Credit Agricole website |
| `ssl_verify` | `bool` | SSL verification flag |

##### Methods
| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `__init__` | - | - | Initializes regional banks manager |
| `by_departement` | `department: int` | `dict` | Retrieves regional bank information by department code. Returns first matching bank or raises exception if none found. |

## Data Structures

### Constants

#### `FAMILLE_PRODUITS` (defined in accounts.py)
```python
[
    {"code": 1, "familleProduit": "COMPTES"},
    {"code": 3, "familleProduit": "EPARGNE_DISPONIBLE"},
    {"code": 7, "familleProduit": "EPARGNE_AUTRE"}
]
```

### Object Structures

#### Account Object
```json
{
    "numeroCompte": "string",
    "index": "string",
    "grandeFamilleProduitCode": "string",
    "libelleProduit": "string",
    "solde": "float",
    "montantEpargne": "float",  // Optional, only for savings accounts
    "devise": "string",
    "dateSolde": "string",
    "typeCompte": "string",
    "statutCompte": "string"
}
```

#### Operation Object Structure
```json
{
    "libelleOperation": "string",
    "dateOperation": "string",
    "montant": "float"
}
```

#### IBAN Object Structure
```json
{
    "ibanData": {
        "ibanData": {
            "ibanCode": "string",
            "bicCode": "string",
            "titulaire": "string",
            "domiciliation": "string",
            "codeGuichet": "string",
            "codeBanque": "string",
            "numeroCompte": "string",
            "cleRib": "string"
        }
    }
}
```

#### Regional Bank Object Structure
```json
{
    "regionalBankUrlPrefix": "string",
    "code": "string",
    "name": "string",
    "department": "string",
    "address": "string",
    "phone": "string",
    "email": "string"
}
```

#### Authentication Response Structure
```json
{
    "keypadId": "string",
    "keyLayout": ["string"]
}
```

#### Deferred Operation Structure
```json
{
    "libelleOperation": "string",
    "dateOperation": "string",
    "montant": "float"
}
```

#### Account Balance Summary Structure
```json
{
    "COMPTES": "float",
    "EPARGNE_DISPONIBLE": "float",
    "EPARGNE_AUTRE": "float"
}
```

#### Card Object Structure
```json
{
    "idCompte": "string",
    "typeCarte": "string",
    "idCarte": "string",
    "titulaire": "string",
    "index": "string"
}
```

Note: All monetary values are returned as floats. Dates are returned in ISO 8601 format (YYYY-MM-DD). String values may be null if the information is not available.