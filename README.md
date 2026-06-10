cat > ~/PIL1_2526_25/README.md << 'EOF'
# IFRI MentorLink — PIL1_2526_25

Application web de mise en relation mentor-mentoré pour les étudiants de l'IFRI — Université d'Abomey-Calavi.

## Description

IFRI_MentorLink est développée dans le cadre du projet intégrateur PIL1 2025-2026. Elle met en relation les étudiants souhaitant offrir ou bénéficier de mentorat académique et professionnel. Chaque utilisateur crée un profil avec ses compétences, sa filière et ses disponibilités. Un algorithme de matching propose automatiquement les paires mentor-mentoré les plus compatibles, tandis qu'une messagerie intégrée temps réel permet d'organiser les sessions.

## Stack technique

- **Backend** : Python 3 · Flask · Flask-SocketIO
- **Base de données** : PostgreSQL
- **Frontend** : HTML · CSS · JavaScript
- **Temps réel** : SocketIO

## Installation

### Prérequis
- Python 3.11+
- PostgreSQL

### Étapes

**1. Cloner le dépôt**
```bash
git clone https://github.com/DavePastore47/PIL1_2526_25.git
cd PIL1_2526_25
```

**2. Créer et activer l'environnement virtuel**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

**3. Installer les dépendances**
```bash
pip install -r requirements.txt
```

**4. Configurer PostgreSQL**
```bash
sudo -u postgres psql
CREATE USER mentorlink WITH PASSWORD 'mentorlink2526';
CREATE DATABASE mentorlink_db OWNER mentorlink;
GRANT ALL PRIVILEGES ON DATABASE mentorlink_db TO mentorlink;
\q
```

**5. Créer les tables**
```bash
psql -U mentorlink -h localhost -d mentorlink_db -f database.sql
```

**6. Insérer les matières IFRI**
```bash
psql -U mentorlink -h localhost -d mentorlink_db -f competences_ifri_EC.sql
```

**7. Insérer les données de test (optionnel)**
```bash
psql -U mentorlink -h localhost -d mentorlink_db -f init_data.sql
```

**8. Lancer l'application**
```bash
python run.py
```

L'application est accessible sur **http://127.0.0.1:5000**

## Comptes et données de test

Des comptes de test sont disponibles. Exécutez `init_data.sql` puis connectez-vous avec n'importe quel email `@ifri.bj` et le mot de passe `test1234`.

| Email | Mot de passe | Filière | Niveau | Rôle |
|-------|-------------|---------|--------|------|
| kofi@ifri.bj | test1234 | GL | L2 | Mentor |
| afi@ifri.bj | test1234 | SI | L1 | Mentoré |
| kader@ifri.bj | test1234 | GL | L3 | Mentor |
| rosine@ifri.bj | test1234 | IA | L2 | Mentor/Mentoré |
| brice@ifri.bj | test1234 | SI | L2 | Mentor |
| laure@ifri.bj | test1234 | GL | L1 | Mentoré |
| armel@ifri.bj | test1234 | IA | L3 | Mentor |
| patrick@ifri.bj | test1234 | SI | L3 | Mentor |
| astride@ifri.bj | test1234 | SI | L2 | Mentor |
| fatima@ifri.bj | test1234 | IA | L1 | Mentoré |

## Groupe 25

| Membre | Rôle |
|--------|------|
| ADJAKA David Geoffroy | Responsable Backend |
| ASSANGBE Yannick | Frontend |
| GBAGUIDI Marie-Merveille | Frontend · Rapport |
| DAGBO Ohèl | Frontend |
| DAHOUE Gracias | Frontend |
| HOUESSOU Armel | Frontend |
| GANHOUNSO Anselme | Frontend |

**Licence 1 — IFRI · UAC · 2025-2026**
EOF
echo "OK"