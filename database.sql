-- Base de données IFRI_MentorLink

-- Suppression des tables si elles existent déjà (dans l'ordre inverse des dépendances)
DROP TABLE IF EXISTS messages CASCADE;
DROP TABLE IF EXISTS conversations CASCADE;
DROP TABLE IF EXISTS matchings CASCADE;
DROP TABLE IF EXISTS offre_competences CASCADE;
DROP TABLE IF EXISTS offres_mentorat CASCADE;
DROP TABLE IF EXISTS utilisateur_competences CASCADE;
DROP TABLE IF EXISTS competences CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;

-- Table utilisateurs
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telephone VARCHAR(20) NOT NULL UNIQUE,
    mot_de_passe VARCHAR(255) NOT NULL,
    filiere VARCHAR(50),
    niveau VARCHAR(20),
    bio TEXT,
    disponibilites TEXT,
    photo VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table competences
CREATE TABLE competences (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    categorie VARCHAR(100)
);

-- Table utilisateur_competences
CREATE TABLE utilisateur_competences (
    id SERIAL PRIMARY KEY,
    utilisateur_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    competence_id INT NOT NULL REFERENCES competences(id) ON DELETE CASCADE,
    type VARCHAR(10) NOT NULL CHECK (type IN ('fort', 'faible'))
);

-- Table offres_mentorat
CREATE TABLE offres_mentorat (
    id SERIAL PRIMARY KEY,
    utilisateur_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    type VARCHAR(10) NOT NULL CHECK (type IN ('offre', 'demande')),
    format VARCHAR(20) CHECK (format IN ('presentiel', 'enligne', 'les deux')),
    disponibilites TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table offre_competences
CREATE TABLE offre_competences (
    id SERIAL PRIMARY KEY,
    offre_id INT NOT NULL REFERENCES offres_mentorat(id) ON DELETE CASCADE,
    competence_id INT NOT NULL REFERENCES competences(id) ON DELETE CASCADE
);

-- Table matchings
CREATE TABLE matchings (
    id SERIAL PRIMARY KEY,
    mentor_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    mentore_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    score FLOAT NOT NULL,
    statut VARCHAR(20) DEFAULT 'propose' CHECK (statut IN ('propose', 'accepte', 'refuse')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table conversations
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    utilisateur1_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    utilisateur2_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table messages
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    expediteur_id INT NOT NULL REFERENCES utilisateurs(id) ON DELETE CASCADE,
    contenu TEXT NOT NULL,
    envoye_a TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    lu BOOLEAN DEFAULT FALSE
);