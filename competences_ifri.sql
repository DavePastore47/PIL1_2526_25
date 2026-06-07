-- ============================================================
-- IFRI MentorLink — Insertion des matières
-- PIL1_2526_25 · IFRI · Université d'Abomey-Calavi
-- ============================================================

-- Suppression et réinsertion propre
TRUNCATE TABLE competences RESTART IDENTITY CASCADE;

-- ============================================================
-- TRONC COMMUN (Semestres 1 et 2)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Logique, arithmétique et applications', 'Tronc commun'),
('Mathématiques fondamentales', 'Tronc commun'),
('Probabilités et statistiques', 'Tronc commun'),
('Architecture et topologie des réseaux informatiques', 'Tronc commun'),
('Système d exploitation et outils de bases en informatique', 'Tronc commun'),
('Bases de la programmation', 'Tronc commun'),
('Déontologie et droit liés aux TIC', 'Tronc commun'),
('Technique d expression écrite et orale', 'Tronc commun'),
('Administration des réseaux sous Windows/Linux', 'Tronc commun'),
('Convergence et calcul différentiel', 'Tronc commun'),
('Mathématiques appliquées', 'Tronc commun'),
('Technologies web et infographie', 'Tronc commun'),
('Bases de données relationnelles', 'Tronc commun'),
('Programmation Python', 'Tronc commun'),
('Anglais technique', 'Tronc commun');

-- ============================================================
-- GÉNIE LOGICIEL (GL)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Structures algébriques et applications en informatique', 'GL'),
('Approche orientée objet', 'GL'),
('Structures de données et applications avec C/Python', 'GL'),
('Programmation avancée en Java', 'GL'),
('Programmation graphique en Qt/C++', 'GL'),
('Aspects avancés des technologies web', 'GL'),
('Bases du génie logiciel', 'GL'),
('Programmation avancée en Python et R', 'GL'),
('Programmation et manipulation des données', 'GL'),
('Système d information décisionnelle et sécurité', 'GL'),
('Génie logiciel', 'GL'),
('Cycle de vie d un logiciel et assurance qualité', 'GL'),
('Gestion des projets', 'GL'),
('Développement avancé d applications web', 'GL'),
('Développement d applications mobiles', 'GL');

-- ============================================================
-- SÉCURITÉ INFORMATIQUE (SI)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Administration systèmes et réseaux', 'SI'),
('Analyse et conception orientées objet', 'SI'),
('Sécurité des systèmes informatiques', 'SI'),
('Management de la sécurité du système d information', 'SI'),
('Sécurité des réseaux', 'SI'),
('Politique de sécurité des systèmes d information', 'SI'),
('Commutation et routage', 'SI'),
('Audit, normes de sécurité et gestion des risques', 'SI'),
('Sécurité des réseaux sans fil', 'SI'),
('Cryptographie et applications', 'SI'),
('Systèmes de détection et de prévention d intrusions', 'SI');

-- ============================================================
-- INTERNET ET MULTIMÉDIA (IM)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Programmation graphique, événementielle et Java entreprise', 'IM'),
('Programmation C#', 'IM'),
('Science fondamentale pour le multimédia', 'IM'),
('Ergonomie et applications e-commerce', 'IM'),
('Expérience utilisateur / Interface utilisateur', 'IM'),
('Pratique des SGBD avancés et le web', 'IM'),
('Production audiovisuelle et jeux vidéos', 'IM'),
('Techniques de dessin et art appliqué', 'IM'),
('Infographie 2D et 3D', 'IM'),
('Technologies immersives', 'IM');

-- ============================================================
-- INTELLIGENCE ARTIFICIELLE (IA)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Statistiques et probabilités pour la science des données', 'IA'),
('Concept et application de l intelligence artificielle', 'IA'),
('Big data', 'IA'),
('Outils cloud de collecte et de traitement de données', 'IA'),
('Concepts et applications de l apprentissage automatique', 'IA'),
('Techniques de résolution de problèmes par la recherche', 'IA'),
('Développement d applications basées sur l apprentissage automatique', 'IA'),
('Corporation Data analytics', 'IA'),
('Outils de résolution de problèmes d optimisation', 'IA');

-- ============================================================
-- SYSTÈMES EMBARQUÉS ET IoT (SE & IoT)
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Électricité et Électronique', 'SE&IoT'),
('Automates programmables et asservissement', 'SE&IoT'),
('Capteurs et actionneurs', 'SE&IoT'),
('Traitement du signal', 'SE&IoT'),
('Langages de description', 'SE&IoT'),
('Architecture des processeurs et microcontrôleurs', 'SE&IoT'),
('Réseaux sans fil et protocoles de communication en IoT', 'SE&IoT'),
('Programmation système, réseau et temps réel', 'SE&IoT'),
('Architecture et intercommunication d un réseau de capteurs', 'SE&IoT'),
('Administration d un réseau de capteurs et IoT', 'SE&IoT');

-- ============================================================
-- MASTER GL
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Architecture logicielle', 'Master GL'),
('Spécification des logiciels', 'Master GL'),
('Méthodes d analyse et de conception', 'Master GL'),
('Algorithmes avancés', 'Master GL'),
('Théorie des langages', 'Master GL'),
('Assurance qualité et test logiciels', 'Master GL'),
('Sécurisation des bases de données et des programmes', 'Master GL'),
('Systèmes répartis et mobiles', 'Master GL'),
('Introduction aux réseaux de neurones artificiels', 'Master GL'),
('Data Mining', 'Master GL');

-- ============================================================
-- MASTER SI / SIRI
-- ============================================================
INSERT INTO competences (nom, categorie) VALUES
('Sécurité des applications et reverse engineering', 'Master SI'),
('Technologies et pratiques du DevSecOps', 'Master SI'),
('Gouvernance de la sécurité du SI', 'Master SI'),
('Gestion du risque et des incidents', 'Master SI'),
('Technologie de la Blockchain et Applications', 'Master SI'),
('Audit de Sécurité du SI', 'Master SI'),
('Technologie et sécurité du Cloud Computing', 'Master SI'),
('Sécurité Web (OWASP)', 'Master SI'),
('Sécurité Mobile (OWASP)', 'Master SI'),
('Administration des serveurs Linux', 'Master SI'),
('Administration des serveurs Windows', 'Master SI');
