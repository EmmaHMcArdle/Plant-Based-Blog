import secrets
import os
from PIL import Image
from flask import render_template, url_for, abort, session, redirect, request, flash
from blog import app, db, bcrypt
from blog.models import Blogpost, User
from blog.forms import RegistrationForm, LoginForm, UpdateAccountForm, StarRatingForm
import sqlalchemy
from blog.config import admin_username, admin_pw
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

@app.route("/post/<string:slug>", methods=["GET", "POST"])
def post(slug):
    form = StarRatingForm()
    if form.validate_on_submit():
        # request.form.get("rating")
        print(form.stars.data)
    else:
        print(form.errors)
    try:
        post = Blogpost.query.filter_by(slug=slug).one()
        return render_template("post.html", post=post, form=form)
    except sqlalchemy.orm.exc.NoResultFound:
        # Allows you to reise an error
        abort(404)

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == admin_username and request.form.get("password") == admin_pw:
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

def save_picture(form_picture):
    #create random hex as to not collide with names of other photos
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    # save within our static folder, app.root_path gives us the whole path
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)
    # TO DO: maybe let people edit the photo's positioning and not make it look bad if not a square
    # TO DO: Delete photos that are no longer being used by users when they change
    output_size = (125, 125)
    form_picture_resized = Image.open(form_picture)
    form_picture_resized.thumbnail(output_size)
    form_picture_resized.save(picture_path)

    return picture_filename

@app.route('/account', methods=['GET', 'POST'])
# decorator
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        # Sends a get request rather than another post so there is no form refresh message
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account",
                          image_file=image_file, form=form)