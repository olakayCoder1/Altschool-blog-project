import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate 
from configurations import config_dict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
path = os.getcwd()
app = Flask(__name__)
app.config.from_object(config_dict['dev'])
db = SQLAlchemy(app)
migrate = Migrate(app=app , db=db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 
login_manager.login_view = "login"


from myblog import routes