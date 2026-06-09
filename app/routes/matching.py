from flask import Blueprint, request, jsonify, session, render_template, redirect
from app.models.matching import (
    get_mentors_potentiels,
    sauvegarder_matching,
    get_matchings_utilisateur,
    mettre_a_jour_statut_matching
)

matching = Blueprint('matching', __name__)


@matching.route('/matching', methods=['GET'])
def page_matching():
    if 'utilisateur_id' not in session:
        return redirect('/page-connexion')
    return render_template('matching.html')


@matching.route('/api/matching', methods=['GET'])
def trouver_mentors():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']
    mentors = get_mentors_potentiels(db, utilisateur_id)
    if not mentors:
        return jsonify({'message': 'Aucun mentor trouvé', 'mentors': []}), 200
    return jsonify({'mentors': mentors}), 200


@matching.route('/matching', methods=['POST'])
def creer_matching():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    data = request.get_json()
    mentor_id = data.get('mentor_id')
    score = data.get('score', 0)
    mentore_id = session['utilisateur_id']
    if not mentor_id:
        return jsonify({'erreur': 'mentor_id requis'}), 400
    result = sauvegarder_matching(db, mentor_id, mentore_id, score)
    return jsonify({
        'message': 'Matching sauvegardé',
        'id': result['id']
    }), 201


@matching.route('/matching/mes-matchings', methods=['GET'])
def mes_matchings():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']
    matchings = get_matchings_utilisateur(db, utilisateur_id)
    return jsonify({
        'matchings': [dict(m) for m in matchings]
    }), 200


@matching.route('/matching/<int:matching_id>', methods=['PUT'])
def mettre_a_jour_matching(matching_id):
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401
    db = request.environ.get('db')
    data = request.get_json()
    statut = data.get('statut')
    if statut not in ['accepte', 'refuse']:
        return jsonify({'erreur': 'Statut invalide'}), 400
    mettre_a_jour_statut_matching(db, matching_id, statut)
    return jsonify({'message': f'Matching {statut}'}), 200