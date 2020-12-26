from flask import Flask, render_template, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/emmamcardle/programming_projects/vegan_blog/blog.db'
# You can't use the database without a secret key
app.config['SECRET_KEY'] = 'mysecretkey'
db = SQLAlchemy(app)

admin = Admin(app)

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # string of max 50 characters
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(100))
    author = db.Column(db.String(25))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    slug = db.Column(db.String(255))

#adding a modelview
admin.add_view(ModelView(Blogpost, db.session))

# posts = [
#     {
#         'author': 'Emma McArdle',
#         'title': 'Best Plant-Based Ice Cream',
#         'byline': "I selflessly tried every vegan ice cream to find the best one, so you don't have to.",
#         'content': "The best brand is by far, Ben & Jerry's. I would honestly just recommend making your own.",
#         'date_posted': 'December 15, 2020'
#     },
#     {
#         'author': 'Emma McArdle',
#         'title': 'Best Plant-Based Sweets',
#         'byline': "I consumed irreversible amounts of sugar, so you don't have to.",
#         'content': "Sour Scandinavian Swimmers",
#         'date_posted': 'December 16, 2020'
#     }
# ]

@app.route("/")
@app.route("/home")
def index():
    # Order post from newest to oldest
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    # In our template, we'll have access to our variable posts
    return render_template("index.html" , posts=posts)
 
@app.route("/about")
def about():
    return render_template("about.html", title="About Page")

@app.route("/post/<string:slug>")
def post(slug):
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post)
    except sqlalchemy.orm.exc.NoResultFound:
        # Allows you to reise an error
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)