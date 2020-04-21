import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf import CSRFProtect  # if you want to enable CSRF protect, uncomment this line
from flask_cors import CORS

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder='templates')
app.config['SECRET_KEY'] = 'secret123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

bcrypt = Bcrypt(app)
cors = CORS(app)

login_manager = LoginManager(app)
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'is-info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'password_email'

mail = Mail(app)
csrf = CSRFProtect(app)  # if you want to enable CSRF protect, uncomment this line

# Register blueprints
from portal.admin.routes import admin
from portal.guru.routes import guru
from portal.jadwal.routes import jadwal

app.register_blueprint(admin)
app.register_blueprint(guru)
app.register_blueprint(jadwal)