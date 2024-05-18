import os

FLASK_ENV = os.getenv('FLASK_ENV')
SECRET_KEY = os.getenv('SECRET_KEY')
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')

DEBUG = True

if FLASK_ENV == 'production':
    DEBUG = False

class AppConfig:
    DEBUG = DEBUG
    SECRET_KEY = SECRET_KEY
    MYSQL_HOST = MYSQL_HOST
    MYSQL_USER =  MYSQL_USER
    MYSQL_PASSWORD = MYSQL_PASSWORD
    MYSQL_DB = MYSQL_DB
    UPLOAD_FOLDER = "./app/uploads"
