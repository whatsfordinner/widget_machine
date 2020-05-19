import logging
import os
from flask import Flask, jsonify, make_response
from logging.config import dictConfig

def create_app():
    configure_logging()
    # creating the application
    app = Flask(__name__, instance_relative_config=True)

    if app.env == 'development':
        logging.getLogger().setLevel(logging.DEBUG)

    # making sure that instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # load in app configuration
    from api import config
    app.config.from_object(config.Config)


    from api import db
    db.init_app(app)

    register_blueprints(app)

    from api import errors
    errors.register_errors(app)

    return app

def register_blueprints(app):
    logging.info('registering blueprints')
    from api import widgets, orders
    app.register_blueprint(widgets.bp)
    app.register_blueprint(orders.bp)

def configure_logging():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '%(asctime)s %(levelname)s [%(name)s] %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })
