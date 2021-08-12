from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admins, db
from auth.auth import auth as auth_blueprint
from core.main import main as main_blueprint
from models import db,Admins
from flask_login import LoginManager
from flask_login import login_user, logout_user, login_required
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
     create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies,get_csrf_token
)
#jwt_refresh_token_required,

app = Flask(__name__)
db.init_app(app)
app.config['SECRET_KEY'] = '2021secrete'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@db/Clientes'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/Clientes'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
# Configure application to store JWTs in cookies
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# Only allow JWT cookies to be sent over https. In production, this
# should likely be True
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_ACCESS_COOKIE_PATH'] = '/api'
app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
app.config['JWT_COOKIE_CSRF_PROTECT'] = True
app.config['JWT_CSRF_IN_COOKIES'] = True
app.config['JWT_SECRET_KEY'] = '2021secrete'  # Change this!

jwt = JWTManager(app)

# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
app.register_blueprint(main_blueprint)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(AdminID):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Admins.query.get(int(AdminID))
