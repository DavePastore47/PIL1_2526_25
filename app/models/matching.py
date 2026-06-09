def get_mentors_potentiels(db, utilisateur_id):
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            u.id,
            u.nom,
            u.prenom,
            u.filiere,
            u.niveau,
            u.bio,
            u.disponibilites,
            COUNT(uc_mentor.competence_id) AS score_base,
            CASE
                WHEN u.filiere = (
                    SELECT filiere FROM utilisateurs WHERE id = %s
                ) THEN COUNT(uc_mentor.competence_id) + 2
                ELSE COUNT(uc_mentor.competence_id)
            END AS score_total
        FROM utilisateurs u
        JOIN utilisateur_competences uc_mentor
            ON uc_mentor.utilisateur_id = u.id
            AND uc_mentor.type = 'fort'
        JOIN utilisateur_competences uc_moi
            ON uc_moi.competence_id = uc_mentor.competence_id
            AND uc_moi.utilisateur_id = %s
            AND uc_moi.type = 'faible'
        WHERE u.id != %s
        GROUP BY u.id, u.nom, u.prenom, u.filiere, u.niveau, u.bio, u.disponibilites
        ORDER BY score_total DESC
    """, (utilisateur_id, utilisateur_id, utilisateur_id))
    mentors = cursor.fetchall()

    result = []
    for mentor in mentors:
        m = dict(mentor)
        cursor.execute("""
            SELECT c.nom
            FROM utilisateur_competences uc_mentor
            JOIN competences c ON c.id = uc_mentor.competence_id
            JOIN utilisateur_competences uc_moi
                ON uc_moi.competence_id = uc_mentor.competence_id
                AND uc_moi.utilisateur_id = %s
                AND uc_moi.type = 'faible'
            WHERE uc_mentor.utilisateur_id = %s
            AND uc_mentor.type = 'fort'
        """, (utilisateur_id, m['id']))
        matieres = cursor.fetchall()
        m['matieres_communes'] = [mat['nom'] for mat in matieres]
        result.append(m)

    return result


def sauvegarder_matching(db, mentor_id, mentore_id, score):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO matchings (mentor_id, mentore_id, score, statut)
        VALUES (%s, %s, %s, 'propose')
        RETURNING id
    """, (mentor_id, mentore_id, score))
    db.commit()
    return cursor.fetchone()


def get_matchings_utilisateur(db, utilisateur_id):
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            m.id,
            m.score,
            m.statut,
            m.created_at,
            mentor.nom AS mentor_nom,
            mentor.prenom AS mentor_prenom,
            mentor.filiere AS mentor_filiere,
            mentore.nom AS mentore_nom,
            mentore.prenom AS mentore_prenom,
            mentore.filiere AS mentore_filiere
        FROM matchings m
        JOIN utilisateurs mentor ON mentor.id = m.mentor_id
        JOIN utilisateurs mentore ON mentore.id = m.mentore_id
        WHERE m.mentor_id = %s OR m.mentore_id = %s
        ORDER BY m.created_at DESC
    """, (utilisateur_id, utilisateur_id))
    return cursor.fetchall()


def mettre_a_jour_statut_matching(db, matching_id, statut):
    cursor = db.cursor()
    cursor.execute("""
        UPDATE matchings SET statut = %s WHERE id = %s
    """, (statut, matching_id))
    db.commit()
