from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from yourapp import db, bcrypt
from yourapp.models import User, Room
from yourapp.forms import RegistrationForm, LoginForm, RoomForm

main_routes = Blueprint('main_routes', __name__)

@main_routes.route("/")
@main_routes.route("/home")
def home():
    return render_template('home.html')

@main_routes.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main_routes.login'))
    return render_template('register.html', title='Register', form=form)

@main_routes.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_routes.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main_routes.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main_routes.home'))

@main_routes.route("/create_room", methods=['GET', 'POST'])
@login_required
def create_room():
    form = RoomForm()
    if form.validate_on_submit():
        room = Room(name=form.name.data, creator=current_user)
        db.session.add(room)
        db.session.commit()
        flash('Your room has been created!', 'success')
        return redirect(url_for('main_routes.home'))
    return render_template('create_room.html', title='Create Room', form=form)

@main_routes.route("/join_room")
@login_required
def join_room():
    return render_template('join_room.html', title='Join Room')
