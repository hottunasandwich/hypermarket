import psycopg2
from flask import current_app, g


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = psycopg2.connect(f"dbname={current_app.config['DB_NAME']} "
                                f"user={current_app.config['DB_USER']} "
                                f"password={current_app.config['DB_PASS']}")

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.commit()
        db.close()


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
