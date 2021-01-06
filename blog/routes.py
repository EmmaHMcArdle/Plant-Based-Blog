from flask import render_template, url_for, abort, session, redirect, request, flash
from blog import app, db, bcrypt
from blog.models import Blogpost, User, Rating
from blog.forms import RegistrationForm, LoginForm
import sqlalchemy
from flask_mail import Mail, Message
from blog.config import mail_username, mail_password
from flask_login import login_user, current_user, logout_user, login_required

app.config['MAIL_SERVER'] = "smtp-mail.outlook.com"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SLS'] = False
app.config['MAIL_USERNAME'] = mail_username
app.config['MAIL_PASSWORD'] = mail_password

mail = Mail(app)

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Your accound has been created! You are now able to log in.', 'success')
        return redirect( url_for('index'))
    return render_template('register.html', title="Registration", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            # after logging in we can try to get the next parameter from the URL
            # get is better than using next as a key because it's optional - If it doesn't exist, next_page will be None
            next_page = request.args.get('next')
            # Ternary Conditional 
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash("Login Unsuccessful. Please check email and password.", 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account')
# decorator
@login_required
def account():
    return render_template('account.html', title="Account")