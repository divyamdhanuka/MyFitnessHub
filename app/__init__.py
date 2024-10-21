from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from flask_bcrypt import Bcrypt
import pandas as pd


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "wassupbro"
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

exercise_data = pd.read_csv("exercise_dataset.csv")

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from app import routes, models
