# Documentation de la Bibliothèque Python du Crédit Agricole

Client Python pour les endpoints JCR du Crédit Agricole permettant d'extraire les informations bancaires d'un compte utilisateur authentifié.

## Table des Matières

1. [Introduction](#introduction)
   - [Authentification](#authentification)
   - [Fonctionnalités de Mock pour les Tests](#fonctionnalités-de-mock-pour-les-tests)
   - [Tests](#tests)
2. [Architecture JCR](#architecture-jcr)
   - [Operations](#operations)
   - [DeferredOperations](#deferredoperations)
   - [Iban](#iban)
   - [Cards](#cards)
   - [Accounts](#accounts)
3. [Modules](#modules)
   - [accounts.py](#accountspy)
     - [Account](#account)
     - [Accounts](#accounts-1)
   - [authenticator.py](#authenticatorpy)
     - [Authenticator](#authenticator)
   - [cards.py](#cardspy)
     - [Card](#card)
     - [Cards](#cards-1)
   - [iban.py](#ibanpy)
     - [Iban](#iban-1)
   - [logout.py](#logoutpy)
     - [Logout](#logout)
   - [operations.py](#operationspy)
     - [DeferredOperations](#deferredoperations-1)
     - [Operation](#operation)
     - [Operations](#operations-1)
   - [regionalbanks.py](#regionalbankspy)
     - [RegionalBankAlias](#regionalbankalias-1)
     - [RegionalBankData](#regionalbankdata-1)
   - [mockconfig.py](#mockconfigpy)
     - [MockConfig](#mockconfig)
4. [Références](#références)
   - [Familles de Produits](#familles-de-produits)

## Introduction

Cette bibliothèque fournit une interface Python aux endpoints JCR du Crédit Agricole. Elle implémente un client qui interagit avec les endpoints JCR de l'interface web du Crédit Agricole pour extraire les informations bancaires d'un compte utilisateur authentifié.

La bibliothèque est conçue pour :
- S'authentifier auprès du service bancaire
- Extraire les informations des comptes via les endpoints JCR
- Récupérer les opérations bancaires
- Gérer les cartes bancaires
- Obtenir les informations IBAN
- Gérer les banques régionales

### Fonctionnalités de Mock pour les Tests

La bibliothèque intègre des fonctionnalités de mocking pour faciliter les tests sans connexion réelle à l'API du Crédit Agricole:

- **Mode Mock**: Quand `useMocksDir` est défini, la bibliothèque utilise des fichiers JSON locaux au lieu de faire des requêtes HTTP
- **Écriture de Mocks**: Quand `writeMocksDir` est défini, les réponses de l'API sont sauvegardées localement dans le répertoire spécifié
- **Structure des Mocks**: Les fichiers de mock sont nommés selon leur fonctionnalité avec des suffixes configurables (ex: `accounts-1_mock.json`, `cards_mock.json`, etc.)
- **Répertoires des Mocks**: 
  - `useMocksDir` : Répertoire où sont lues les réponses mockées
  - `writeMocksDir` : Répertoire où sont écrites les réponses mockées
- **Suffixes des Mocks**: 
  - `useMockSuffix` : Suffixe ajouté aux noms des fichiers mock lors de la lecture (par défaut "mock")
  - `writeMockSuffix` : Suffixe ajouté aux noms des fichiers mock lors de l'écriture (par défaut "mock")

Ces fonctionnalités sont particulièrement utiles pour:
- Les tests unitaires et d'intégration sans connexion réelle aux services bancaires
- Le développement et le débogage en environnement hors ligne
- Les démonstrations où l'accès aux vraies données bancaires n'est pas souhaitable

Pour une documentation détaillée des fichiers mock et leur utilisation, consultez la [Documentation des Mocks](/mocks/README.md).

### Authentification

L'authentification est gérée via la classe [`Authenticator`](#authenticator) qui :
- Gère la session utilisateur
- Détermine la banque régionale appropriée
- Maintient les cookies de session
- Gère le processus d'authentification sécurisée

### Tests

La bibliothèque inclut une suite de tests complète avec :
- Tests unitaires pour les composants individuels
- Tests d'intégration pour les interactions avec les endpoints JCR
- Tests simulés pour le développement hors ligne
- Rapports de couverture utilisant pytest-cov

## Architecture JCR

La bibliothèque interagit avec les points d'accès JCR du Crédit Agricole. Toutes les requêtes sont effectuées sur le domaine principal du Crédit Agricole, avec un préfixe spécifique à votre banque régionale.

### URL de Base

```
https://www.credit-agricole.fr/{regional_bank_url_prefix}/particulier/{endpoint}
```

Où :
- `{regional_bank_url_prefix}` : Identifiant unique de votre banque régionale
  - Exemples : `ca-paris`, `ca-normandie-seine`, `ca-sud-mediterranee`
  - Ce préfixe est automatiquement détecté lors de l'authentification
- `{endpoint}` : Point d'accès spécifique à la fonctionnalité souhaitée
  - Format : `jcr:content.{nom_du_service}.json`
  - Exemple : `jcr:content.n3.operations.json` pour les opérations bancaires

### Points d'accès JCR

Les points d'accès JCR sont les interfaces qui permettent d'interagir avec les différentes fonctionnalités du service bancaire en ligne. Chaque point d'accès retourne des données au format JSON et nécessite une authentification préalable. Les points d'accès sont organisés par fonctionnalité (comptes, opérations, cartes, etc.) et suivent une structure cohérente dans leur nommage.

#### Operations

Récupère les opérations d'un compte.

• **Point d'accès :** `jcr:content.n3.operations.json`

• **Paramètres :**
| Paramètre | Description |
|-----------|-------------|
| `grandeFamilleCode` | Code de la famille de produit |
| `compteIdx` | Index du compte |
| `date_start` | Date de début au format YYYY-MM-DD |
| `date_stop` | Date de fin au format YYYY-MM-DD |
| `count` | Nombre maximum d'opérations à récupérer |
| `sleep` | Temps d'attente entre les requêtes paginées |

• **Structure de réponse :**
| Champ | Type | Description |
|-------|------|-------------|
| `dateOp` | `str` | Date de l'opération |
| `descr` | `dict` | Détails complets de l'opération |
| `libelleOp` | `str` | Étiquette de l'opération |
| `montantOp` | `float` | Montant de l'opération |

---

#### DeferredOperations

Récupère les opérations différées d'une carte bancaire.

• **Point d'accès :** `jcr:content.n3.operations.encours.carte.debit.differe.json`

• **Structure de réponse :**
| Champ | Type | Description |
|-------|------|-------------|
| `dateOp` | `str` | Date de l'opération |
| `descr` | `dict` | Détails complets de l'opération |
| `libelleOp` | `str` | Étiquette de l'opération |
| `montantOp` | `float` | Montant de l'opération |

---

#### Iban

Récupère les informations IBAN d'un compte.

• **Point d'accès :** `jcr:content.ibaninformation.json`

• **Paramètres :**
| Paramètre | Description |
|-----------|-------------|
| `compteIdx` | Index du compte |
| `grandeFamilleCode` | Code de la famille de produit |

• **Structure de réponse :**
| Champ | Type | Description |
|-------|------|-------------|
| `iban` | `dict` | Détails IBAN complets |
| `ibanCode` | `str` | Code IBAN |
| `numeroCompte` | `str` | Numéro de compte associé |

---

#### Cards

Récupère la liste des cartes bancaires associées aux comptes.

• **Point d'accès :** `moyens-paiement/gestion-carte-v2/mes-cartes/jcr:content.listeCartesParCompte.json`

• **Structure de réponse :**
| Champ | Type | Description |
|-------|------|-------------|
| `card` | `dict` | Détails complets de la carte |
| `idCarte` | `str` | ID de la carte |
| `idCompte` | `str` | ID du compte associé |
| `titulaire` | `str` | Nom du titulaire |
| `typeCarte` | `str` | Type de carte |

---

#### Accounts

Récupère la synthèse des produits de valorisation.

• **Point d'accès :** `operations/synthese/jcr:content.produits-valorisation.json/{product_code}`

• **Paramètres :**
| Paramètre | Description |
|-----------|-------------|
| `product_code` | Code de la famille de produit |

• **Structure de réponse :**
| Champ | Type | Description |
|-------|------|-------------|
| `account` | `dict` | Détails complets du compte |
| `index` | `str` | Index du compte utilisé dans les requêtes JCR |
| `grandeFamilleProduitCode` | `str` | Code de la famille de produit |
| `numeroCompte` | `str` | Numéro de compte |
| `libelleProduit` | `str` | Libellé du produit |
| `solde` | `float` | Solde du compte |
| `montantEpargne` | `float` | Montant épargne (si applicable) |

---

## Modules

Les modules implémentent la logique métier et gèrent l'interaction avec l'API du Crédit Agricole. Chaque module est responsable d'un aspect spécifique des opérations bancaires.

### accounts.py

#### `Account`

Représente un compte bancaire unique.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `account` | `dict` | Détails du compte |
| `compteIdx` | `str` | Index du compte |
| `grandeFamilleCode` | `str` | Code de la famille de produit |
| `numeroCompte` | `str` | Numéro de compte |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator`<br>`account: dict` | - | Initialise le compte avec la session et les détails |
| `__str__` | - | `str` | Représentation en chaîne du compte |
| `get_iban` | - | [Iban](#iban-1) | Retourne les informations IBAN |
| `get_operations` | `date_start: str = None`<br>`date_stop: str = None`<br>`count: int = 100`<br>`sleep: int \| None = None` | [Operations](#operations-1) | Récupère les opérations du compte. Les paramètres de date sont optionnels et doivent être au format ISO 8601 (YYYY-MM-DD). Si date_stop est None, définit automatiquement la plage de dates sur les 30 derniers jours. Le paramètre count limite le nombre d'opérations retournées. Le paramètre sleep permet de définir un délai entre les requêtes paginées. |
| `as_json` | - | `str` | Retourne les détails du compte en JSON |
| `get_solde` | - | `float` | Retourne le solde du compte (montantEpargne si disponible, sinon solde) |

#### `Accounts`

Gère plusieurs comptes bancaires.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `accounts_list` | `list[Account]` | Liste d'objets Account |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator` | - | Initialise le gestionnaire de comptes et appelle automatiquement get_accounts_per_products() |
| `__iter__` | - | `self` | Permet l'itération sur les comptes |
| `__next__` | - | `Account` | Retourne le prochain compte dans l'itération |
| `search` | `num: str` | `Account` | Recherche un compte par son numéro |
| `as_json` | - | `str` | Retourne la liste des comptes en JSON |
| `get_accounts_per_products` | - | - | Récupère les comptes pour chaque famille de produits |
| `get_solde` | - | `float` | Retourne le solde global de tous les comptes |
| `get_solde_per_products` | - | `dict` | Retourne le solde par famille de produits |

### authenticator.py

#### `Authenticator`

Gère l'authentification utilisateur et la gestion des sessions.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `cookies` | `dict` | Cookies de session |
| `department` | `int` | Code département de l'utilisateur |
| `keypadId` | `str` | ID du clavier pour l'authentification sécurisée |
| `password` | `list[int]` | Mot de passe de connexion de l'utilisateur sous forme de tableau de chiffres |
| `regional_bank_url` | `str` | Préfixe d'URL de la banque régionale |
| `ssl_verify` | `bool` | Drapeau de vérification SSL |
| `url` | `str` | URL de base du site web du Crédit Agricole |
| `username` | `str` | Nom d'utilisateur de connexion |
| `mock_config` | `MockConfig` | Configuration pour les mocks |
| `mocksDir` | `str` | Accesseur pour mock_config.mocksDir |
| `useMocks` | `bool` | Accesseur pour mock_config.useMocks |
| `writeMocks` | `bool` | Accesseur pour mock_config.writeMocks |
| `mockSuffix` | `str` | Accesseur pour mock_config.mockSuffix |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `username: str`<br>`password: list[int]`<br>`department: int`<br>`mock_config: MockConfig = None` | - | Initialise l'authentificateur et effectue l'authentification |
| `find_regional_bank` | `use_local: bool = True` | - | Trouve l'URL de la banque régionale, utilise les alias.json locaux si use_local est True. Lève `Exception` si regionalBankUrlPrefix est manquant. |
| `map_digit` | `key_layout: list[str]`<br>`digit: str` | `int` | Mappe les chiffres à la disposition du clavier |
| `authenticate` | - | - | Effectue le processus d'authentification. Lève `Exception` si l'authentification échoue en raison d'identifiants invalides ou d'erreurs serveur. |

### cards.py

#### `Card`

Représente une carte bancaire unique.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `card` | `dict` | Détails de la carte |
| `idCarte` | `str` | ID de la carte |
| `idCompte` | `str` | ID du compte associé |
| `session` | `Authenticator` | Session d'authentification |
| `titulaire` | `str` | Nom du titulaire de la carte |
| `typeCarte` | `str` | Type de carte |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator`<br>`card: dict` | - | Initialise la carte avec la session et les détails |
| `__str__` | - | `str` | Représentation en chaîne de la carte |
| `get_operations` | - | [DeferredOperations](#deferredoperations-1) | Récupère les opérations différées de la carte. |
| `as_json` | - | `str` | Retourne les détails de la carte en JSON |

#### `Cards`

Gère plusieurs cartes bancaires.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `cards_list` | `list[Card]` | Liste d'objets Card |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator` | - | Initialise le gestionnaire de cartes |
| `__iter__` | - | `Iterator[Card]` | Implémentation de l'itérateur |
| `__next__` | - | [Card](#card) | Prochain élément dans l'itération |
| `as_json` | - | `str` | Retourne toutes les cartes en JSON |
| `search` | `num_last_digits: str` | [Card](#card) | Recherche une carte par les derniers chiffres du numéro de carte (idCarte). La méthode compare si le numéro de carte se termine par les chiffres fournis et retourne l'instance Card correspondante. Lève `Exception` si aucune carte correspondante n'est trouvée. |
| `get_cards_per_account` | - | - | Récupère les cartes groupées par compte et remplit cards_list. Lève `Exception` si la requête API échoue ou si la réponse ne contient pas le champ "comptes" attendu. |

### iban.py

#### `Iban`

Gère les informations IBAN d'un compte.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `compteIdx` | `str` | Index du compte |
| `grandeFamilleCode` | `str` | Code de la famille de produit |
| `iban` | `dict` | Détails IBAN complets |
| `ibanCode` | `str` | Code IBAN |
| `numeroCompte` | `str` | Numéro de compte |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator`<br>`compteIdx: str`<br>`grandeFamilleCode: str`<br>`numeroCompte: str` | - | Initialise le gestionnaire IBAN |
| `__str__` | - | `str` | Représentation en chaîne de l'IBAN |
| `get_iban_data` | - | - | Récupère les informations IBAN de l'API et remplit iban et ibanCode. Lève `Exception` si la requête API échoue. |
| `as_json` | - | `str` | Retourne les détails IBAN en JSON |

### logout.py

#### `Logout`

Gère la déconnexion de l'utilisateur.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator` | - | Initialise l'objet de déconnexion |
| `logout` | - | - | Effectue la déconnexion en appelant l'API de déconnexion. |

### operations.py

#### `DeferredOperations`

Gère les opérations différées d'une carte bancaire.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `operations` | `list[Operation]` | Liste d'objets Operation |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator` | - | Initialise les opérations différées en effectuant une requête à l'API |
| `__iter__` | - | `Iterator[Operation]` | Implémentation de l'itérateur |
| `__next__` | - | [Operation](#operation) | Prochain élément dans l'itération |
| `as_json` | - | `str` | Retourne toutes les opérations différées en JSON |

#### `Operation`

Représente une opération bancaire unique.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `dateOp` | `str` | Date de l'opération |
| `descr` | `dict` | Détails complets de l'opération |
| `libelleOp` | `str` | Étiquette de l'opération |
| `montantOp` | `float` | Montant de l'opération |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `operation: dict` | - | Initialise l'opération avec les détails |
| `__str__` | - | `str` | Représentation en chaîne de l'opération |
| `as_json` | - | `str` | Retourne les détails de l'opération en JSON |

#### `Operations`

Gère plusieurs opérations bancaires.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `operations` | `list[Operation]` | Liste d'objets Operation |
| `session` | `Authenticator` | Session d'authentification |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `session: Authenticator`<br>`compteIdx: str`<br>`grandeFamilleCode: str`<br>`date_start: str = None`<br>`date_stop: str = None`<br>`count: int = 100`<br>`sleep: int \| None = None` | - | Initialise les opérations en effectuant une requête à l'API |
| `__iter__` | - | `Iterator[Operation]` | Implémentation de l'itérateur |
| `__next__` | - | [Operation](#operation) | Prochain élément dans l'itération |
| `as_json` | - | `str` | Retourne toutes les opérations en JSON |

### regionalbanks.py

Ce module est responsable de la gestion des informations sur les banques régionales. Il utilise le fichier `aliases.json` (situé à la racine du package `creditagricole_particuliers`) qui contient un mappage des codes départementaux vers les détails des banques régionales, y compris leurs alias URL.

#### `RegionalBankAlias`

Gère les alias des banques régionales.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `alias` | `str` | Alias de la banque régionale |
| `url` | `str` | URL de la banque régionale |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `alias: str`<br>`url: str` | - | Initialise l'alias de la banque régionale |
| `__str__` | - | `str` | Représentation en chaîne de l'alias de la banque régionale |
| `as_json` | - | `str` | Retourne l'alias de la banque régionale en JSON |

#### `RegionalBankData`

Gère les données des banques régionales.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `regional_bank_alias_list` | `list[RegionalBankAlias]` | Liste d'objets RegionalBankAlias |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | - | - | Initialise les données des banques régionales en chargeant les alias depuis le fichier JSON |
| `__iter__` | - | `Iterator[RegionalBankAlias]` | Implémentation de l'itérateur |
| `__next__` | - | [RegionalBankAlias](#regionalbankalias-1) | Prochain élément dans l'itération |
| `as_json` | - | `str` | Retourne toutes les données des banques régionales en JSON |

### mockconfig.py

#### `MockConfig`

Configure les fonctionnalités de mock pour les tests.

##### Propriétés
| Propriété | Type | Description |
|-----------|------|-------------|
| `useMocksDir` | `str` | Répertoire où sont lues les réponses mockées |
| `writeMocksDir` | `str` | Répertoire où sont écrites les réponses mockées |
| `useMockSuffix` | `str` | Suffixe à ajouter aux noms des fichiers mock lors de la lecture (par défaut "mock") |
| `writeMockSuffix` | `str` | Suffixe à ajouter aux noms des fichiers mock lors de l'écriture (par défaut "mock") |

##### Méthodes
| Méthode | Paramètres | Retourne | Description |
|---------|------------|----------|-------------|
| `__init__` | `useMocksDir: str = None`<br>`writeMocksDir: str = None`<br>`useMockSuffix: str = "mock"`<br>`writeMockSuffix: str = "mock"` | - | Initialise la configuration des mocks |
| `useMocks` | - | `bool` | Indique si les requêtes doivent être mockées (retourne True si useMocksDir est défini) |
| `writeMocks` | - | `bool` | Indique si les réponses doivent être écrites dans les fichiers mock (retourne True si writeMocksDir est défini) |
| `write_json_mock` | `mock_file: str`<br>`content: str \| dict` | `str \| None` | Écrit le contenu JSON dans un fichier mock. Retourne le chemin du fichier créé ou None si writeMocksDir n'est pas défini |
| `read_json_mock` | `mock_file: str` | `str \| None` | Lit le contenu d'un fichier mock. Retourne le contenu du fichier ou None si useMocksDir n'est pas défini |
| `__str__` | - | `str` | Représentation en chaîne de la configuration des mocks |

Pour une documentation détaillée des fichiers mock et leur utilisation, consultez la [Documentation des Mocks](/mocks/README.md).

## Références

### Familles de Produits

| Code | Famille de Produit |
|------|-------------------|
| 1 | COMPTES |
| 3 | EPARGNE_DISPONIBLE |
| 7 | EPARGNE_AUTRE |
