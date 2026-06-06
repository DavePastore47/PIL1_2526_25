from flask import Blueprint, request, jsonify, session
from app.models.utilisateur import creer_utilisateur, get_utilisateur_par_email, verifier_mot_de_passe
from app.models.utilisateur import (
    creer_utilisateur, get_utilisateur_par_email, verifier_mot_de_passe,
    get_utilisateur_par_id, modifier_profil, get_competences,
    supprimer_competences, ajouter_competence
)

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