def creer_conversation(db, utilisateur1_id, utilisateur2_id):

    cursor = db.cursor()
    cursor.execute("""
        SELECT id FROM conversations
        WHERE (utilisateur1_id = %s AND utilisateur2_id = %s)
        OR (utilisateur1_id = %s AND utilisateur2_id = %s)
    """, (utilisateur1_id, utilisateur2_id, utilisateur2_id, utilisateur1_id))
    
    existante = cursor.fetchone()
    if existante:

        return existante
    

    cursor.execute("""
        INSERT INTO conversations (utilisateur1_id, utilisateur2_id)
        VALUES (%s, %s)
        RETURNING id
    """, (utilisateur1_id, utilisateur2_id))
    db.commit()
    return cursor.fetchone()


def get_conversation(db, conversation_id):

    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM conversations WHERE id = %s
    """, (conversation_id,))
    return cursor.fetchone()


def get_conversations_utilisateur(db, utilisateur_id):

    cursor = db.cursor()
    cursor.execute("""
        SELECT
            c.id,
            c.created_at,
            -- Nom de l'interlocuteur
            CASE
                WHEN c.utilisateur1_id = %s THEN u2.nom || ' ' || u2.prenom
                ELSE u1.nom || ' ' || u1.prenom
            END AS interlocuteur,
            -- Id de l'interlocuteur
            CASE
                WHEN c.utilisateur1_id = %s THEN c.utilisateur2_id
                ELSE c.utilisateur1_id
            END AS interlocuteur_id,
            -- Dernier message
            (
                SELECT contenu FROM messages
                WHERE conversation_id = c.id
                ORDER BY envoye_a DESC LIMIT 1
            ) AS dernier_message,
            -- Nombre de messages non lus
            (
                SELECT COUNT(*) FROM messages
                WHERE conversation_id = c.id
                AND expediteur_id != %s
                AND lu = FALSE
            ) AS non_lus
        FROM conversations c
        JOIN utilisateurs u1 ON u1.id = c.utilisateur1_id
        JOIN utilisateurs u2 ON u2.id = c.utilisateur2_id
        WHERE c.utilisateur1_id = %s OR c.utilisateur2_id = %s
        ORDER BY c.created_at DESC
    """, (utilisateur_id, utilisateur_id, utilisateur_id, utilisateur_id, utilisateur_id))
    return cursor.fetchall()


def envoyer_message(db, conversation_id, expediteur_id, contenu):

    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO messages (conversation_id, expediteur_id, contenu)
        VALUES (%s, %s, %s)
        RETURNING id, envoye_a
    """, (conversation_id, expediteur_id, contenu))
    db.commit()
    return cursor.fetchone()


def get_messages_conversation(db, conversation_id):

    cursor = db.cursor()
    cursor.execute("""
        SELECT
            m.id,
            m.contenu,
            m.envoye_a,
            m.lu,
            m.expediteur_id,
            u.nom AS expediteur_nom,
            u.prenom AS expediteur_prenom
        FROM messages m
        JOIN utilisateurs u ON u.id = m.expediteur_id
        WHERE m.conversation_id = %s
        ORDER BY m.envoye_a ASC
    """, (conversation_id,))
    return cursor.fetchall()


def marquer_messages_lus(db, conversation_id, utilisateur_id):

    cursor = db.cursor()
    cursor.execute("""
        UPDATE messages
        SET lu = TRUE
        WHERE conversation_id = %s
        AND expediteur_id != %s
        AND lu = FALSE
    """, (conversation_id, utilisateur_id))
    db.commit()