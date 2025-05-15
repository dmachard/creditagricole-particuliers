# Exemples de la Bibliothèque Python du Crédit Agricole

Ce document explique comment exécuter les scripts d'exemple fournis dans ce répertoire.

## Pour Commencer

Avant d'exécuter des exemples, assurez-vous d'avoir configuré votre environnement :

1. Créez et activez un environnement virtuel :
   ```bash
   # Créer l'environnement virtuel
   python -m venv venv
   
   # Activer sur Linux/Mac
   source venv/bin/activate
   
   # Ou activer sur Windows
   .\venv\Scripts\activate
   ```

2. Installez les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Exemples Disponibles {#examples-section}

Les scripts d'exemple suivants sont disponibles dans ce répertoire :

### 1. Gestion des Comptes
- Fichier : [accounts_example.py](./accounts_example.py)
- Description : Montre comment lister tous vos comptes et leurs détails.
- Exécution :
  ```bash
  python accounts_example.py
  ```

### 2. Opérations de Compte
- Fichier : [account_operations_example.py](./account_operations_example.py)
- Description : Démontre comment récupérer et afficher les opérations de vos comptes.
- Exécution :
  ```bash
  python account_operations_example.py
  ```

### 3. Gestion des Cartes
- Fichier : [cards_example.py](./cards_example.py)
- Description : Montre comment gérer et afficher les détails de vos cartes de crédit/débit.
- Exécution :
  ```bash
  python cards_example.py
  ```

### 4. Banques Régionales
- Fichier : [regional_banks_example.py](./regional_banks_example.py)
- Description : Affiche les informations sur les banques régionales du Crédit Agricole.
- Exécution :
  ```bash
  python regional_banks_example.py
  ```

## Exécution des Exemples

Lors de l'exécution de ces exemples :

1. Vous serez invité à saisir vos identifiants Crédit Agricole :
   - Nom d'utilisateur
   - Mot de passe (saisi de manière sécurisée)
   - Code département (par exemple, 75 pour Paris)

2. Les exemples géreront automatiquement :
   - L'authentification sécurisée
   - La gestion appropriée des sessions
   - La déconnexion sécurisée une fois terminé

3. Si vous rencontrez des erreurs :
   - Vérifiez votre connexion Internet
   - Vérifiez vos identifiants
   - Assurez-vous d'utiliser le bon code département

## Module Utilitaires

Le fichier [`_utils.py`](./_utils.py) contient des fonctions d'aide utilisées par les exemples. Vous n'avez pas besoin d'exécuter ce fichier directement.
