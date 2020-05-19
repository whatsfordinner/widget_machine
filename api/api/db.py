import logging
import mysql.connector
from mysql.connector import errorcode
from flask import current_app, g
from time import time_ns

logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user=current_app.config['DB_USER'],
            password=current_app.config['DB_PASS'],
            host=current_app.config['DB_HOST'],
            database=current_app.config['DB_NAME']
        )
    
    def close(self):
        self.cnx.close()

    def execute_query(self, query, params=None):
        cursor = self.cnx.cursor(
            dictionary=True
        )

        logger.debug(f'executing query: {query} with params: {params}')
        cursor.execute(query, params)

        results = []
        for result in cursor:
            results.append(result)

        cursor.close()

        self.cnx.commit()

        return results

def get_db():
    if 'db' not in g:
        logger.debug('Establishing connection to DB')
        try:
            g.db = DatabaseConnection()

        except mysql.connector.Error as err:
            logger.error(f'Unable to connect to DB: {err}')
            raise

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        logger.debug('Closing connection to DB')
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)
