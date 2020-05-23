import logging
import pugsql
from flask import current_app, g

logger = logging.getLogger(__name__)

def get_db():
    if 'db' not in g:
        logger.debug('Establishing new connection to DB')
        g.db = pugsql.module('api/db/queries/')
        g.db.connect(f'mysql+mysqlconnector://{current_app.config["DB_USER"]}:{current_app.config["DB_PASS"]}@{current_app.config["DB_HOST"]}/{current_app.config["DB_NAME"]}')
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        logger.debug('Closing connection to DB')
        db.disconnect()

def init_app(app):
    app.teardown_appcontext(close_db)