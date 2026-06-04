from flask import Flask, g
import psycopg2
from psycopg2.extras import RealDictCursor

def create_app():
    app = Flask(__name__)
    app.secret_key = 'mentorlink_secret_key'

    app.config['DB_CONFIG'] = {
        'host': 'localhost',
        'database': 'mentorlink_db',
        'user': 'mentorlink',
        'password': 'mentorlink2526'
    }

    @app.before_request
    def open_db():
        g.db = psycopg2.connect(
            **app.config['DB_CONFIG'],
            cursor_factory=RealDictCursor
        )
        from flask import request
        request.environ['db'] = g.db

    @app.teardown_request
    def close_db(error):
        db = g.pop('db', None)
        if db is not None:
            if error:
                db.rollback()
            db.close()

    from app.routes.auth import auth
    app.register_blueprint(auth)

    return app