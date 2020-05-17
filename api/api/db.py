import logging
import mysql.connector
from mysql.connector import errorcode
from flask import current_app, g

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

        cursor.execute(query, params)

        results = []
        for result in cursor:
            results.append(result)

        cursor.close()

        self.cnx.commit()

        return results

def get_db():
    if 'db' not in g:
        logging.info('Establishing connection to DB')
        try:
            g.db = DatabaseConnection()

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
