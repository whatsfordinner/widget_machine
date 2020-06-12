import logging
import os
from flask import Flask, jsonify, make_response
from logging.config import dictConfig
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

def create_app():
    """ Create the application using Flask's application factory pattern """

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

def build_callable():
    """ Create a WSGI callable application that incorporate the Prometheus /metrics endpoint """

    return DispatcherMiddleware(
        create_app(),
        {
            '/metrics': make_wsgi_app()
        }
    )

def register_blueprints(app):
    """ Register the blueprints that represent the /widgets and /orders endpoints to the Flask application """

    logging.info('registering blueprints')
    from api import widgets, orders
    app.register_blueprint(widgets.bp)
    app.register_blueprint(orders.bp)

def configure_logging():
    """ Configure Python logging to match the desired format
        TODO: file logging - should this be handled by uwsgi?
    """

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
