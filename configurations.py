import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

BASE_DIR=os.path.dirname(os.path.realpath(__file__))


UPLOAD_FOLDER = 'static/uploads'
class Config:
    SECRET_KEY=os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS=True 
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}



class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite3' )
    UPLOAD_FOLDER = UPLOAD_FOLDER 
    EMAIL_SENDER_MAIL = os.getenv('EMAIL_SENDER') 
    EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_PASSWORD') 
    # UPLOAD_FOLDER = os.path.join( BASE_DIR, 'media' )


class ProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS=False


config_dict = {
    'dev': DevelopmentConfig ,
    'pro' : ProductionConfig ,
    'test': TestingConfig
}