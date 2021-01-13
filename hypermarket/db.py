import psycopg2
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(f"dbname={current_app.config['DB_NAME']} "
                                f"user={current_app.config['DB_USER']} "
                                f"password={current_app.config['DB_PASS']}")

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.commit()
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)
