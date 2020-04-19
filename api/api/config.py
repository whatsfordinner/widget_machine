import os

class Config:
    # General configuration
    SECRET_KEY = os.environ.get('WIDGET_API_SECRET_KEY', 'dev')

    # Database configuration
    DB_HOST = os.environ.get('WIDGET_DB_HOST', 'localhost')
    DB_USER = os.environ.get('WIDGET_DB_USER', 'widgets')
    DB_PASS = os.environ.get('WIDGET_DB_PASS', 'password')
    DB_NAME = os.environ.get('WIDGET_DB_NAME', 'widgets')
