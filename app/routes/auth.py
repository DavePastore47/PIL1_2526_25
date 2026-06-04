from flask import Blueprint, request, jsonify, session
from app.models.utilisateur import creer_utilisateur, get_utilisateur_par_email, verifier_mot_de_passe

auth = Blueprint('auth', __name__)

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