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