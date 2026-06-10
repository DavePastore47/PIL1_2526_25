from flask import session
from flask_socketio import join_room, leave_room, emit
from app import socketio
import psycopg2
from psycopg2.extras import RealDictCursor


def get_db():
    conn = psycopg2.connect(
        "host=localhost dbname=mentorlink_db user=mentorlink password=mentorlink2526",
        cursor_factory=RealDictCursor
    )
    return conn


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
    from app.models.message import envoyer_message
    conversation_id = data.get('conversation_id')
    contenu = data.get('contenu')
    expediteur_id = session.get('utilisateur_id')

    if not all([conversation_id, contenu, expediteur_id]):
        return

    db = None
    try:
        db = get_db()
        message = envoyer_message(db, conversation_id, expediteur_id, contenu)
        db.commit()
        emit('nouveau_message', {
            'conversation_id': conversation_id,
            'expediteur_id': expediteur_id,
            'contenu': contenu,
            'envoye_a': str(message['envoye_a']),
            'id': message['id']
        }, room=f'conv_{conversation_id}')
    except Exception as e:
        print(f"Erreur SocketIO: {e}")
        if db:
            db.rollback()
    finally:
        if db:
            db.close()