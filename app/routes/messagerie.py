from app.models.utilisateur import get_utilisateur_par_id, get_competences
from flask import redirect
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

@messagerie.route('/profil-page')
def page_profil():
    if 'utilisateur_id' not in session:
        return redirect('/connexion')
    return render_template('profil.html')