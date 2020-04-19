import logging
import mysql.connector
from mysql.connector import errorcode
from flask import current_app, g

def get_db():
    if 'db' not in g:
        logging.info('Establishing connection to DB')
        try:
            g.db = mysql.connector.connect(
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASS'],
                host=current_app.config['DB_HOST'],
                database=current_app.config['DB_NAME']
            )

        except mysql.connector.Error as err:
            logging.error(f'Unable to connect to DB: {err}')
            raise

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
