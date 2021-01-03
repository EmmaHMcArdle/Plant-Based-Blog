from flask import Flask, render_template, url_for, abort, session, redirect, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import sqlalchemy
from flask_mail import Mail, Message
from config import mail_username, mail_password, secret_key
from forms import RegistrationForm, LoginForm


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/emmamcardle/programming_projects/vegan_blog/blog.db'
# You can't use the database without a secret key 
# A secret key will protect against modifying cookies and cross-site request forgery attacks
app.config['SECRET_KEY'] = secret_key
app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SLS'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mail = Mail(app)
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
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')

        msg = Message(subject=f"Mail from {name}", body=f"Name: {name}\nE-Mail: {email}\nPhone: {phone}\n\n\n{message}", sender=mail_username, recipients=['AntonVego@gmail.com'])
        mail.send(msg)
        return render_template("contact.html", success=True)
    return render_template("contact.html", title="Contact Us")

@app.route("/post/<string:slug>")
def post(slug):
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post)
    except sqlalchemy.orm.exc.NoResultFound:
        # Allows you to reise an error
        abort(404)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == "emma" and request.form.get("password") == "emma@12345":
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template("admin_login.html", failed=True)
    return render_template("admin_login.html")

@app.route("/admin_logout")
def admin_logout():
    session.clear()
    return redirect('/')

@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect( url_for('index'))
    return render_template('register.html', title="Registration", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check username and password", 'danger')
    return render_template('login.html', title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True)