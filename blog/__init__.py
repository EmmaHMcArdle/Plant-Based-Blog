from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from blog.config import secret_key

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/emmamcardle/programming_projects/vegan_blog/blog.db'
# You can't use the database without a secret key 
# A secret key will protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = secret_key

db = SQLAlchemy(app)

from blog import routes