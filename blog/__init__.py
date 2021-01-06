from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blog.config import secret_key
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/emmamcardle/programming_projects/vegan_blog/blog.db'
# You can't use the database without a secret key 
# A secret key will protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
from blog import routes