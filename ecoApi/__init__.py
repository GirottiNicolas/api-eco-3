from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Configurar la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#'mysql+pymysql://nicolas:1234@localhost/ecoProject'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar SQLAlchemy
db = SQLAlchemy()

migrate = Migrate(app, db)

login_manager = LoginManager(app)

# Le aclaramos a login_manager donde esta ubicada la ruta de inicio de sesion
login_manager.login_view = 'login'

from ecoApi import routes
