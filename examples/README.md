# Documentation des Exemples

## Table des Matières

1. [Introduction](#introduction)
2. [Exemples Disponibles](#exemples-disponibles)
   - [Exemple Standard](#exemple-standard)
   - [Exemple de Recherche](#exemple-de-recherche)
3. [Utilisation des Mocks](#utilisation-des-mocks)
   - [Configuration des Mocks](#configuration-des-mocks)
   - [Utilisation des Données Réelles](#utilisation-des-données-réelles)
4. [Structure des Exemples](#structure-des-exemples)
   - [Authentification](#authentification)
   - [Gestion des Sessions](#gestion-des-sessions)
   - [Gestion des Erreurs](#gestion-des-erreurs)

## Introduction

Cette documentation décrit les exemples fournis avec la bibliothèque Python du Crédit Agricole. Ces exemples démontrent comment utiliser les différentes fonctionnalités de la bibliothèque pour interagir avec les services bancaires en ligne.

## Exemples Disponibles

### Exemple Standard

Le fichier `standard_example.py` illustre les cas d'utilisation standard de l'API :

- Authentification et création de session
- Récupération des informations de la banque régionale
- Liste de tous les comptes et leurs détails :
  - Informations du compte et IBAN
  - Opérations récentes sur une période donnée
  - Solde actuel
- Liste de toutes les cartes et leurs opérations différées
- Gestion propre de la déconnexion

Cet exemple couvre les fonctionnalités les plus fréquemment utilisées, mais ne représente pas l'ensemble des possibilités offertes par l'API. Pour des cas d'utilisation plus spécifiques, consultez la documentation complète de la bibliothèque.

### Exemple de Recherche

Le fichier `search_example.py` montre comment rechercher des éléments spécifiques :

- Recherche d'un compte par son numéro
- Recherche d'une carte par ses 4 derniers chiffres

## Utilisation des Mocks

### Configuration des Mocks

Les exemples utilisent par défaut des données mockées pour éviter d'effectuer de véritables appels API. La configuration des mocks se fait via la classe `MockConfig` :

```python
mock_config = MockConfig(
    useMocksDir=mocks_dir,      # Répertoire contenant les fichiers mock
    writeMocksDir=None,         # Pas d'écriture de données mock
    useMockSuffix="mock",       # Suffixe des fichiers mock
    writeMockSuffix="mock"      # Suffixe pour les nouveaux fichiers mock
)
```

### Utilisation des Données Réelles

Pour utiliser les données réelles au lieu des mocks :

1. Supprimez la configuration des mocks :
```python
session = Authenticator(
    username=username,
    password=password_digits,
    department=department
)
```

2. Assurez-vous d'avoir les identifiants corrects :
- `username` : Votre numéro client Crédit Agricole
- `password_digits` : Votre mot de passe à 6 chiffres
- `department` : Votre numéro de département

## Structure des Exemples

### Authentification

Tous les exemples commencent par l'authentification :

```python
session = Authenticator(
    username=username,
    password=password_digits,
    department=department,
    mock_config=mock_config
)
```

### Gestion des Sessions

Les exemples utilisent un bloc `try/finally` pour garantir une déconnexion propre :

```python
try:
    # Code d'utilisation de l'API
finally:
    Logout(session).logout()
```

### Gestion des Erreurs

Les exemples incluent une gestion basique des erreurs avec des messages de log. Pour une utilisation en production, il est recommandé d'ajouter une gestion d'erreurs plus robuste.

## Bonnes Pratiques

1. **Sécurité**
   - Ne stockez jamais les identifiants en dur dans le code
   - Utilisez des variables d'environnement ou des fichiers de configuration sécurisés
   - Déconnectez-vous toujours après utilisation

2. **Performance**
   - Limitez le nombre d'opérations récupérées avec le paramètre `count`
   - Utilisez des plages de dates appropriées pour les opérations
   - Évitez les appels API inutiles

3. **Développement**
   - Utilisez les mocks pendant le développement
   - Testez avec des données réelles avant la mise en production
   - Documentez les cas d'erreur spécifiques à votre utilisation
