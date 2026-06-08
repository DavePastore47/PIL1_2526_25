from flask import session, request
from flask_socketio import join_room, leave_room, emit
from app import socketio
from app.models.message import envoyer_message


@socketio.on('rejoindre_conversation')
def on_rejoindre(data):
    conversation_id = data.get('conversation_id')
    join_room(f'conv_{conversation_id}')


@socketio.on('quitter_conversation')
def on_quitter(data):
    conversation_id = data.get('conversation_id')
    leave_room(f'conv_{conversation_id}')


@socketio.on('envoyer_message')
def on_message(data):
    conversation_id = data.get('conversation_id')
    contenu = data.get('contenu')
    expediteur_id = session.get('utilisateur_id')

    if not all([conversation_id, contenu, expediteur_id]):
        return

    from flask import g
    db = g.get('db')
    if not db:
        return

    message = envoyer_message(db, conversation_id, expediteur_id, contenu)

    emit('nouveau_message', {
        'conversation_id': conversation_id,
        'expediteur_id': expediteur_id,
        'contenu': contenu,
        'envoye_a': str(message['envoye_a']),
        'id': message['id']
    }, room=f'conv_{conversation_id}')