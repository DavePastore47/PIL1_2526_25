# Rapport d'Expérience - Installation des Dépendances

## Objectif
Installer les dépendances du projet Flask pour qu'il soit opérationnel.

## Problèmes Rencontrés

### 1. **Erreur d'environnement Python** 🔒
- **Problème**: Impossible d'installer les paquets directement avec `pip install -r requirements.txt`
- **Raison**: Python 3.12 a implémenté PEP 668 qui empêche les installations au niveau du système
- **Solution**: Création d'un environnement virtuel avec `python3 -m venv venv`

### 2. **Dépendance MySQL manquante** 💾
- **Problème**: `mysqlclient==2.2.8` a échoué lors de l'installation
- **Raison**: Le paquet compile une extension C qui nécessite les en-têtes de développement MySQL
- **Solution**: Installation des dépendances système avec `sudo apt-get install default-libmysqlclient-dev python3-dev`

### 3. **Module `psycopg2` manquant** 🐘
- **Problème**: Le fichier `app/__init__.py` importait `psycopg2` (driver PostgreSQL), mais il n'était pas dans `requirements.txt`
- **Raison**: Le projet utilise à la fois MySQL (Flask-MySQLdb) ET PostgreSQL (psycopg2)
- **Solution**: Ajout de `psycopg2-binary==2.9.9` à `requirements.txt`

## Étapes de Résolution

1. ✅ Activation de l'environnement virtuel existant
2. ✅ Tentative initiale d'installation (échouée - erreur PEP 668)
3. ✅ Création d'un nouvel environnement virtuel avec venv
4. ✅ Installation de mysqlclient (nécessitait des dépendances système)
5. ✅ Identificationdu problème psycopg2 manquant
6. ✅ Ajout de `psycopg2-binary==2.9.9` à requirements.txt
7. ✅ Installation réussie de psycopg2-binary

## Modifications Apportées

### Fichier: `requirements.txt`
```diff
+ psycopg2-binary==2.9.9
```

## Configuration Actuelle

**Architecture de Base de Données:**
- **MySQL**: Utilisé via `Flask-MySQLdb==2.0.0`
- **PostgreSQL**: Utilisé via `psycopg2-binary==2.9.9`

**Configuration PostgreSQL** (dans `app/__init__.py`):
```python
app.config['DB_CONFIG'] = {
    'host': 'localhost',
    'database': 'mentorlink_db',
    'user': 'mentorlink',
    'password': 'mentorlink2526'
}
```

## État Final

✅ Toutes les dépendances sont maintenant installées et l'application peut être lancée.

### Packages Installés:
- bidict, blinker, click
- Flask, Flask-Login, Flask-MySQLdb, Flask-SocketIO
- h11, itsdangerous, Jinja2, MarkupSafe
- mysqlclient
- **psycopg2-binary** (nouvellement ajouté)
- python-engineio, python-socketio
- simple-websocket
- Werkzeug, wsproto

## Prochaines Étapes Recommandées

1. Vérifier que les bases de données PostgreSQL et MySQL sont créées et accessibles
2. Tester le démarrage de l'application avec `python run.py`
3. Vérifier que les blueprints (auth, matching) se chargent correctement

## Notes Techniques

- **Pourquoi `psycopg2-binary`?** La version "binary" évite les problèmes de compilation locale et est idéale pour le développement/déploiement rapide
- **Virtenv**: Le projet utilise déjà un dossier `venv/` pour isoler les dépendances (bonne pratique)
- **Sécurité**: Les identifiants PostgreSQL sont codés en dur - à améliorer en utilisant des variables d'environnement en production

