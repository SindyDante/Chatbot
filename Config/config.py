import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask application configuration
    FLASK_APP = 'app.py'
    FLASK_ENV = 'development'
    DEBUG = True

    # Database configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gunicorn configuration
    GUNICORN_PORT = 8000
    GUNICORN_WORKERS = 4