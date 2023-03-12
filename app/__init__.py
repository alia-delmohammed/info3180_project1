import os
from flask import Flask
from app.config import Config
from flask_migrate import Migrate 
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'Som3$ec5etK*y'
db = SQLAlchemy(app)

from app import views
from app import models

migrate = Migrate(app, db)

# set the UPLOAD_FOLDER and allowed extensions for uploaded files
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# create the UPLOAD_FOLDER if it doesn't exist
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])