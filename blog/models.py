from blog import db, app, login_manager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from flask import abort, session
from flask_login import UserMixin


admin = Admin(app)

# naming convention for extension
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # string of max 50 characters
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(25))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    slug = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    # Our rating attribute has a relationship to the post model
    # backref is similar to adding another column to the post model
    # lazy = True means that sqlalchemy will load the data as neccesary in one go
    # will be able to get all ratings created by a user
    # not a column but an additional query in the background 
    ratings = db.relationship('Rating', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Rating('{self.stars}', '{self.review}')"

# Will inherit from ModelView class
class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            # means your unauthorized
            abort(403)

#adding a modelview
admin.add_view(SecureModelView(Blogpost, db.session))