# Documentation des Fichiers Mock pour Crédit Agricole Particuliers

## Table des Matières

1. [Introduction](#introduction)
2. [Structure des Fichiers Mock](#structure-des-fichiers-mock)
3. [Types de Fichiers Mock](#types-de-fichiers-mock)
4. [Utilisation des Mocks](#utilisation-des-mocks)

## Introduction

Cette documentation décrit le système de fichiers mock utilisé par la bibliothèque Python Crédit Agricole Particuliers. Les fichiers mock permettent de simuler les réponses de l'API du Crédit Agricole sans effectuer de véritables requêtes HTTP.

## Structure des Fichiers Mock

Les fichiers mock sont des fichiers JSON qui contiennent les réponses de l'API. Ils sont nommés selon un schéma qui reflète leur fonctionnalité:

```
[fonctionnalité]_[suffixe].json
```

ou, pour les fonctionnalités liées à un compte ou une carte spécifique:

```
[type]-[identifiant]_[fonctionnalité]_[suffixe].json
```

## Types de Fichiers Mock

### Fichiers Mock pour l'Authentification

**Nom de fichier**: `authentication_keypad_{suffixe}.json` et `authentication_security_{suffixe}.json`

**Description**: Contient les réponses du serveur pour les étapes d'authentification (disposition du clavier et vérification de sécurité).

### Fichiers Mock pour les Banques Régionales

**Nom de fichier**: `regionalbank-{department}_{suffixe}.json`

**Description**: Contient les informations sur une banque régionale pour un département spécifique.

### Fichiers Mock pour les Comptes

**Nom de fichier**: `accounts-{grandeFamilleCode}_{suffixe}.json`

**Description**: Contient les informations sur les comptes d'une famille de produits spécifique.

### Fichiers Mock pour les Opérations

**Nom de fichier**: `account-{grandeFamilleCode}-{compteIdx}_operations_{suffixe}.json`

**Description**: Contient les opérations bancaires pour un compte spécifique.

### Fichiers Mock pour les Opérations de Carte

**Nom de fichier**: `card-{carteIdx}_operations_{suffixe}.json`

**Description**: Contient les opérations différées pour une carte bancaire spécifique.

### Fichiers Mock pour les Cartes

**Nom de fichier**: `cards_{suffixe}.json`

**Description**: Contient la liste des cartes bancaires associées aux comptes.

### Fichiers Mock pour les IBAN

**Nom de fichier**: `account-{grandeFamilleCode}-{compteIdx}_iban_{suffixe}.json`

**Description**: Contient les informations IBAN pour un compte spécifique.

### Fichiers Mock pour la Déconnexion

**Nom de fichier**: `logout_{suffixe}.json`

**Description**: Contient la réponse de l'API lors de la déconnexion. Ce fichier est optionnel car la déconnexion peut fonctionner sans mock.

## Utilisation des Mocks

Les fichiers mock sont utilisés pour:

1. **Développement Hors Ligne**
   - Permettre le développement sans connexion internet
   - Éviter les limitations de l'API en production
   - Accélérer le cycle de développement

2. **Démonstrations**
   - Présenter les fonctionnalités sans accès aux vrais comptes
   - Montrer des exemples de données réalistes
   - Éviter les problèmes de confidentialité

3. **Débogage**
   - Reproduire des scénarios spécifiques
   - Tester des cas d'erreur particuliers
   - Valider le comportement avec des données connues

4. **Documentation**
   - Fournir des exemples de réponses API
   - Documenter la structure des données
   - Servir de référence pour l'intégration

5. **Tests Automatisés**
   - Permettre l'exécution de tests sans dépendance à l'API
   - Garantir la reproductibilité des tests
   - Faciliter l'intégration continue (CI/CD)
   - Tester des scénarios spécifiques de manière fiable
   - Valider le comportement avec des données contrôlées 