from flask import Flask, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from config import Config

import os
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
# from app.models import User
# from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
app.config.from_object(Config)


csrf = CSRFProtect(app)
csrf.init_app(app)

db = SQLAlchemy(app)
# db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

#  конечная для входа в систему
login_manager.login_view = 'login'

bcrypt = Bcrypt(app)

@login_manager.user_loader
def user_loader(user_id):
    ptint(f'from init {user_id}')
    return User.query.get(user_id)

from app import routes, models, forms
# db.create_all()
