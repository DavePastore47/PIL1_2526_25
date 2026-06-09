from flask import Blueprint, request, jsonify, session, render_template, redirect
from app.models.message import (
    creer_conversation,
    get_conversation,
    get_conversations_utilisateur,
    envoyer_message,
    get_messages_conversation,
    marquer_messages_lus
)
from app.models.utilisateur import get_utilisateur_par_id, get_competences

messagerie = Blueprint('messagerie', __name__)


@messagerie.route('/conversations', methods=['GET'])
def mes_conversations():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401

    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']

    conversations = get_conversations_utilisateur(db, utilisateur_id)
    return jsonify({
        'conversations': [dict(c) for c in conversations]
    }), 200


@messagerie.route('/conversations', methods=['POST'])
def nouvelle_conversation():
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401

    db = request.environ.get('db')
    data = request.get_json()
    utilisateur2_id = data.get('utilisateur_id')

    if not utilisateur2_id:
        return jsonify({'erreur': 'utilisateur_id requis'}), 400

    conversation = creer_conversation(db, session['utilisateur_id'], utilisateur2_id)
    return jsonify({
        'message': 'Conversation créée',
        'conversation_id': conversation['id']
    }), 201


@messagerie.route('/conversations/<int:conversation_id>/messages', methods=['GET'])
def voir_messages(conversation_id):
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401

    db = request.environ.get('db')
    utilisateur_id = session['utilisateur_id']

    marquer_messages_lus(db, conversation_id, utilisateur_id)

    messages = get_messages_conversation(db, conversation_id)
    return jsonify({
        'messages': [dict(m) for m in messages]
    }), 200


@messagerie.route('/conversations/<int:conversation_id>/messages', methods=['POST'])
def envoyer(conversation_id):
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401

    db = request.environ.get('db')
    data = request.get_json()
    contenu = data.get('contenu')

    if not contenu:
        return jsonify({'erreur': 'Le message ne peut pas être vide'}), 400

    message = envoyer_message(db, conversation_id, session['utilisateur_id'], contenu)
    return jsonify({
        'message': 'Message envoyé',
        'id': message['id'],
        'envoye_a': str(message['envoye_a'])
    }), 201


@messagerie.route('/profil/<int:user_id>')
def voir_profil_utilisateur(user_id):
    if 'utilisateur_id' not in session:
        return jsonify({'erreur': 'Non connecté'}), 401

    db = request.environ.get('db')
    utilisateur = get_utilisateur_par_id(db, user_id)
    competences = get_competences(db, user_id)

    return jsonify({
        'id': utilisateur['id'],
        'nom': utilisateur['nom'],
        'prenom': utilisateur['prenom'],
        'bio': utilisateur['bio'],
        'competences': [dict(c) for c in competences]
    }), 200


@messagerie.route('/chat')
def page_chat():
    if 'utilisateur_id' not in session:
        return redirect('/page-connexion')
    return render_template('message.html')


@messagerie.route('/profil-page')
def page_profil():
    if 'utilisateur_id' not in session:
        return redirect('/page-connexion')
    return render_template('interface/profil.html')