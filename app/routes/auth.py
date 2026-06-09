from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.models.utilisateur import (
    creer_utilisateur, get_utilisateur_par_email, verifier_mot_de_passe,
    get_utilisateur_par_id, modifier_profil, get_competences,
    supprimer_competences, ajouter_competence
)

auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
@auth.route('/accueil', methods=['GET'])
@auth.route('/', methods=['GET'])
@auth.route('/accueil', methods=['GET'])
def accueil():
    connecte = 'utilisateur_id' in session
    nom = session.get('nom', '')
    return render_template('accueil.html', connecte=connecte, nom=nom)

@auth.route('/apropos', methods=['GET'])
def apropos():
    return render_template('apropos.html')

@auth.route('/page-connexion', methods=['GET'])
def page_connexion():
    return render_template('connexion.html')

@auth.route('/page-inscription', methods=['GET'])
def page_inscription():
    return render_template('inscription.html')

@auth.route('/inscription', methods=['POST'])
def inscription():
    db = request.environ.get('db')
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')
    mot_de_passe = data.get('mot_de_passe')
    filiere = data.get('filiere')
    niveau = data.get('niveau')
    if not all([nom, prenom, email, telephone, mot_de_passe]):
        return jsonify({'erreur': 'Champs obligatoires manquants'}), 400
    existant = get_utilisateur_par_email(db, email)
    if existant:
        return jsonify({'erreur': 'Email déjà utilisé'}), 409
    utilisateur = creer_utilisateur(db, nom, prenom, email, telephone, mot_de_passe, filiere, niveau)
    return jsonify({'message': 'Inscription réussie', 'id': utilisateur['id']}), 201


@auth.route('/connexion', methods=['POST'])
def connexion():
    db = request.environ.get('db')
    data = request.get_json()
    email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    if not all([email, mot_de_passe]):
        return jsonify({'erreur': 'Email et mot de passe requis'}), 400
    utilisateur = get_utilisateur_par_email(db, email)
    if not utilisateur:
        return jsonify({'erreur': 'Email ou mot de passe incorrect'}), 401
    if not verifier_mot_de_passe(utilisateur['mot_de_passe'], mot_de_passe):
        return jsonify({'erreur': 'Email ou mot de passe incorrect'}), 401
    session['utilisateur_id'] = utilisateur['id']
    session['nom'] = utilisateur['nom']
    return jsonify({'message': 'Connexion réussie', 'nom': utilisateur['nom']}), 200


@auth.route('/deconnexion', methods=['POST'])
def deconnexion():
    session.clear()
    return jsonify({'message': 'Déconnexion réussie'}), 200


@auth.route('/profil', methods=['GET'])
def voir_profil():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']
    utilisateur = get_utilisateur_par_id(db, utilisateur_id)
    competences = get_competences(db, utilisateur_id)
    return jsonify({
        'id': utilisateur['id'],
        'nom': utilisateur['nom'],
        'prenom': utilisateur['prenom'],
        'email': utilisateur['email'],
        'filiere': utilisateur['filiere'],
        'niveau': utilisateur['niveau'],
        'bio': utilisateur['bio'],
        'disponibilites': utilisateur['disponibilites'],
        'competences': [dict(c) for c in competences]
    }), 200


@auth.route('/profil', methods=['PUT'])
def modifier_profil_route():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    filiere = data.get('filiere')
    niveau = data.get('niveau')
    bio = data.get('bio', '')
    disponibilites = data.get('disponibilites', '')
    competences = data.get('competences', [])
    if not all([nom, prenom]):
        return jsonify({'erreur': 'Nom et prénom obligatoires'}), 400
    modifier_profil(db, utilisateur_id, nom, prenom, filiere, niveau, bio, disponibilites)
    supprimer_competences(db, utilisateur_id)
    for comp in competences:
        ajouter_competence(db, utilisateur_id, comp['nom'], comp['type'])
    return jsonify({'message': 'Profil mis à jour avec succès'}), 200

@auth.route('/parametres', methods=['GET'])
def page_parametres():
    if 'utilisateur_id' not in session:
        return redirect('/page-connexion')
    return render_template('parametres.html')

@auth.route('/compte/email', methods=['PUT'])
def changer_email():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    data = request.get_json()
    nouvel_email = data.get('email')
    mot_de_passe = data.get('mot_de_passe')
    if not all([nouvel_email, mot_de_passe]):
        return jsonify({'erreur': 'Email et mot de passe requis'}), 400
    utilisateur = get_utilisateur_par_id(db, session['utilisateur_id'])
    if not verifier_mot_de_passe(utilisateur['mot_de_passe'], mot_de_passe):
        return jsonify({'erreur': 'Mot de passe incorrect'}), 401
    cursor = db.cursor()
    cursor.execute("UPDATE utilisateurs SET email = %s WHERE id = %s", (nouvel_email, session['utilisateur_id']))
    db.commit()
    return jsonify({'message': 'Email mis à jour'}), 200

@auth.route('/compte/telephone', methods=['PUT'])
def changer_telephone():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    data = request.get_json()
    nouveau_tel = data.get('telephone')
    mot_de_passe = data.get('mot_de_passe')
    if not all([nouveau_tel, mot_de_passe]):
        return jsonify({'erreur': 'Téléphone et mot de passe requis'}), 400
    utilisateur = get_utilisateur_par_id(db, session['utilisateur_id'])
    if not verifier_mot_de_passe(utilisateur['mot_de_passe'], mot_de_passe):
        return jsonify({'erreur': 'Mot de passe incorrect'}), 401
    cursor = db.cursor()
    cursor.execute("UPDATE utilisateurs SET telephone = %s WHERE id = %s", (nouveau_tel, session['utilisateur_id']))
    db.commit()
    return jsonify({'message': 'Téléphone mis à jour'}), 200

@auth.route('/compte/mot-de-passe', methods=['PUT'])
def changer_mot_de_passe():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    data = request.get_json()
    ancien = data.get('ancien_mot_de_passe')
    nouveau = data.get('nouveau_mot_de_passe')
    if not all([ancien, nouveau]):
        return jsonify({'erreur': 'Ancienne et nouvelle mot de passe requis'}), 400
    if len(nouveau) < 6:
        return jsonify({'erreur': 'Le mot de passe doit contenir au moins 6 caractères'}), 400
    utilisateur = get_utilisateur_par_id(db, session['utilisateur_id'])
    if not verifier_mot_de_passe(utilisateur['mot_de_passe'], ancien):
        return jsonify({'erreur': 'Ancien mot de passe incorrect'}), 401
    from werkzeug.security import generate_password_hash
    nouveau_hash = generate_password_hash(nouveau)
    cursor = db.cursor()
    cursor.execute("UPDATE utilisateurs SET mot_de_passe = %s WHERE id = %s", (nouveau_hash, session['utilisateur_id']))
    db.commit()
    return jsonify({'message': 'Mot de passe mis à jour'}), 200