from werkzeug.security import generate_password_hash, check_password_hash

def creer_utilisateur(db, nom, prenom, email, telephone, mot_de_passe, filiere, niveau):
    cursor = db.cursor()
    mot_de_passe_hash = generate_password_hash(mot_de_passe)
    cursor.execute("""
        INSERT INTO utilisateurs (nom, prenom, email, telephone, mot_de_passe, filiere, niveau)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
    """, (nom, prenom, email, telephone, mot_de_passe_hash, filiere, niveau))
    db.commit()
    return cursor.fetchone()

def get_utilisateur_par_email(db, email):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE email = %s", (email,))
    return cursor.fetchone()

def get_utilisateur_par_id(db, id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM utilisateurs WHERE id = %s", (id,))
    return cursor.fetchone()

def verifier_mot_de_passe(mot_de_passe_hash, mot_de_passe):
    return check_password_hash(mot_de_passe_hash, mot_de_passe)

def modifier_profil(db, utilisateur_id, nom, prenom, filiere, niveau, bio, disponibilites):
    
    cursor = db.cursor()
    cursor.execute("""
        UPDATE utilisateurs
        SET nom=%s, prenom=%s, filiere=%s, niveau=%s, bio=%s, disponibilites=%s
        WHERE id=%s
    """, (nom, prenom, filiere, niveau, bio, disponibilites, utilisateur_id))
    db.commit()

def get_competences(db, utilisateur_id):
    
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.nom, uc.type
        FROM utilisateur_competences uc
        JOIN competences c ON c.id = uc.competence_id
        WHERE uc.utilisateur_id = %s
    """, (utilisateur_id,))
    return cursor.fetchall()

def supprimer_competences(db, utilisateur_id):
    
    cursor = db.cursor()
    cursor.execute("""
        DELETE FROM utilisateur_competences WHERE utilisateur_id = %s
    """, (utilisateur_id,))
    db.commit()

def ajouter_competence(db, utilisateur_id, nom_competence, type_competence):
    
    cursor = db.cursor()
    cursor.execute("SELECT id FROM competences WHERE nom = %s", (nom_competence,))
    competence = cursor.fetchone()

    if not competence:
        
        cursor.execute("""
            INSERT INTO competences (nom) VALUES (%s) RETURNING id
        """, (nom_competence,))
        competence_id = cursor.fetchone()['id']
    else:
        competence_id = competence['id']

    
    cursor.execute("""
        INSERT INTO utilisateur_competences (utilisateur_id, competence_id, type)
        VALUES (%s, %s, %s)
    """, (utilisateur_id, competence_id, type_competence))
    db.commit()