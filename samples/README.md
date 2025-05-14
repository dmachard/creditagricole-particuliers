# Utilisation des Exemples de Données du Crédit Agricole

## Table des matières
- [Introduction](#introduction)
- [Fichiers de Données d'Exemple](#fichiers-de-données-dexemple)
  - [Mode de données](#mode-de-données)
  - [Mode de types](#mode-de-types)
- [Script de Création d'Exemples](#script-de-création-dexemples)
  - [Prérequis](#prérequis)
  - [Utilisation](#utilisation)
  - [Arguments de Ligne de Commande](#arguments-de-ligne-de-commande)
  - [Exemples](#exemples)
  - [Fonctionnement](#fonctionnement)
  - [Considérations de Sécurité](#considérations-de-sécurité)
- [Utilisation des Données d'Exemple pour le Développement](#utilisation-des-données-dexemple-pour-le-développement)
- [Mise à Jour des Exemples](#mise-à-jour-des-exemples)

## Introduction

Cette documentation explique comment utiliser les fichiers de données d'exemple et les outils fournis avec la bibliothèque `creditagricole-particuliers` pour faciliter le développement et les tests.

## Fichiers de Données d'Exemple

Le dossier `/data` contient des fichiers JSON qui représentent les structures de données renvoyées par le service du Crédit Agricole. Deux modes d'extraction sont disponibles, créant différents formats de fichiers :

### Mode de données

Ce mode (par défaut) extrait vos données réelles et les sauvegarde sans suffixe. Ces fichiers contiennent toutes vos informations financières.

- **Fichiers de Collection** :
  - `accounts.json` : Liste complète des comptes
  - `cards.json` : Liste complète des cartes
  - `regionalBanks.json` : Liste des banques régionales et leurs départements

- **Fichiers Individuels** :
  - `account_{numéro_compte}.json` : Détails spécifiques pour chaque compte
  - `account_{numéro_compte}_operations.json` : Historique des opérations pour chaque compte
  - `account_{numéro_compte}_iban.json` : Coordonnées IBAN pour chaque compte
  - `card_{4_derniers_chiffres}.json` : Détails spécifiques pour chaque carte
  - `card_{4_derniers_chiffres}_operations.json` : Historique des opérations pour chaque carte
  - `regionalBank_{code_département}.json` : Informations sur la banque régionale d'un département

### Mode de types

Ce mode (`--mode types`) extrait uniquement la structure des données avec des valeurs fictives en fonction des types de données. Les valeurs sont remplacées par :
- Pour les chaînes : "" (chaîne vide)
- Pour les nombres entiers : 0
- Pour les nombres décimaux : 0.0
- Pour les booléens : false
- Pour les listes : un seul élément exemple

Ces fichiers portent le suffixe `_types` et sont idéaux pour le développement sans manipuler de données personnelles. Les identifiants numériques dans les noms de fichiers sont remplacés par des zéros pour préserver la confidentialité.

- **Fichiers de Collection** :
  - `accounts_types.json` : Structure des comptes (un seul exemple)
  - `cards_types.json` : Structure des cartes (un seul exemple)

- **Fichiers Individuels** :
  - `account_000000_types.json` : Structure des détails d'un compte (les zéros remplacent le vrai numéro de compte)
  - `account_000000_operations_types.json` : Structure des opérations (un seul exemple)
  - `card_0000_types.json` : Structure des détails d'une carte (les zéros remplacent les vrais chiffres)
  - `card_0000_operations_types.json` : Structure des opérations carte (un seul exemple)
  - `regionalBank_00_types.json` : Structure des informations bancaires (les zéros remplacent le vrai code département)

## Script de Création d'Exemples

Le script `create_samples.py` se connecte à votre espace Crédit Agricole et récupère les données via la bibliothèque. Il est utile pour :

1. Comprendre la structure complète des données disponibles
2. Obtenir des exemples réels pour vos tests
3. Vérifier si la structure des réponses du service a changé
4. Générer une documentation de la structure des API sans exposer vos données financières

### Prérequis

- Vos identifiants Crédit Agricole (identifiant, mot de passe et code département)
- Python 3.6 ou version plus récente
- La bibliothèque `creditagricole-particuliers` installée

### Utilisation

Vous pouvez exécuter le script de plusieurs manières :

1. En mode "data" (défaut) avec mot de passe en ligne de commande :
```bash
./create_samples.py --username VOTRE_IDENTIFIANT --password VOTRE_MOT_DE_PASSE --department VOTRE_CODE_DEPARTEMENT
```

2. En mode "types" avec saisie sécurisée du mot de passe :
```bash
./create_samples.py --username VOTRE_IDENTIFIANT --department VOTRE_CODE_DEPARTEMENT --mode types
```

### Arguments de Ligne de Commande

- `--username` : Votre identifiant Crédit Agricole (obligatoire)
- `--password` : Votre mot de passe Crédit Agricole (composé de chiffres). Si non fourni, il sera demandé de façon sécurisée
- `--department` : Votre code département (nombre entier, obligatoire)
- `--output-dir` : Dossier de destination pour les fichiers générés (par défaut : ./data pour le mode data, ./types pour le mode types)
- `--mode` : Mode d'extraction des données (options : data, types ; défaut : data)
  - `data` : Extrait vos données réelles (sensibles)
  - `types` : Extrait uniquement la structure avec des valeurs fictives

### Exemples

Exécution simple (utilise le mode "data" par défaut et sauvegarde dans le répertoire ./data) :
```bash
./create_samples.py --username johndoe --department 75
```

Extraction des données réelles avec paramètres explicites :
```bash
./create_samples.py --username johndoe --department 75 --mode data --output-dir ./customData
```

Extraction des structures de type uniquement :
```bash
./create_samples.py --username johndoe --department 75 --mode types
```

Pour enregistrer les fichiers dans un dossier personnalisé :
```bash
./create_samples.py --username johndoe --department 75 --output-dir ./mes_exemples
```

### Fonctionnement

1. Le script s'authentifie auprès du Crédit Agricole avec vos identifiants
2. Selon le mode choisi, il extrait soit les données réelles, soit uniquement les structures de type

**Mode 'data'** (défaut) :
- Extrait toutes vos données financières réelles
- Sauvegarde tous les comptes, toutes les cartes, et toutes les opérations
- Fichiers sauvegardés dans le dossier ./data par défaut

**Mode 'types'** :
- Extrait uniquement la structure des données
- Remplace les valeurs réelles par des placeholders selon leur type
- Ne sauvegarde qu'un seul exemple de chaque type de donnée (compte, carte, opération)
- Ajoute le suffixe '_types' aux fichiers
- Fichiers sauvegardés dans le dossier ./types par défaut

3. Les données sont enregistrées au format JSON dans le dossier spécifié

### Considérations de Sécurité

- Le script ne conserve pas vos identifiants
- Exécutez-le uniquement sur un système sécurisé
- Pour éviter d'exposer vos données financières, utilisez le mode 'types' pour le développement et la documentation

## Utilisation des Données d'Exemple pour le Développement

Les fichiers d'exemple peuvent servir pendant le développement à :

1. **Analyser la Structure des Données** : Explorer les champs disponibles dans chaque type de réponse
2. **Créer des Interfaces** : Concevoir des écrans qui affichent correctement les données
3. **Développer Sans Connexion** : Travailler sur votre application sans connexion au service du Crédit Agricole
4. **Automatiser les Tests** : Créer des tests avec des données prévisibles et constantes

Le mode 'types' est particulièrement utile pour:
- Comprendre la structure des API sans exposer des données sensibles
- Partager des exemples dans un dépôt de code
- Créer une documentation technique

## Mise à Jour des Exemples

Pour mettre à jour les fichiers d'exemple :

1. Exécutez le script `create_samples.py` avec vos identifiants et le mode souhaité
2. Vérifiez les fichiers générés dans le dossier de destination
3. Pour les fichiers en mode 'types', vous pouvez les ajouter directement à votre dépôt de code
4. Pour les fichiers en mode 'data', assurez-vous d'anonymiser toute information personnelle avant de les partager

N'oubliez pas d'anonymiser toute information personnelle ou confidentielle avant d'enregistrer ces fichiers dans un système de gestion de versions. 