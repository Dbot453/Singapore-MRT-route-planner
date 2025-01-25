from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
import sqlite3
from . import db

auth = Blueprint('auth', __name__)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_password = request.form.get('password')

        # conn = sqlite3.connect("instance/database.db")
        # c = conn.cursor()
        # c.execute("SELECT * FROM user WHERE email = ?", (email,))
        # database_user = c.fetchone()
        # user_password = database_user[2] if database_user else None
        # conn.close()
        
        user = User.query.filter_by(email=email).first()
        user_password = user.password if user else None
        if user:
            if check_password_hash(user_password, entered_password):
                flash('Logged in successfully!', category='success')
                #flask_user = UserMixin(database_user[0], database_user[1], database_user[2])
                login_user(user, remember=False)
                return redirect(url_for('views.calculate_route'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        conn = sqlite3.connect("instance/database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()

        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            if user:
                flash('Email already exists.', category='error')
            else:
                conn = sqlite3.connect("instance/database.db")
                c = conn.cursor()
                c.execute("INSERT into user (email, first_name, password) values (?, ?, ?)", (email, first_name, generate_password_hash(password1, method='pbkdf2:sha256')))
                conn.commit()
                conn.close()
                # login_user(new_user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)