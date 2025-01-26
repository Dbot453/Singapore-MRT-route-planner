# from flask import Blueprint, render_template, request, flash, redirect, url_for
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import db   ##means from __init__.py import db
# from flask_login import login_user, login_required, logout_user, current_user, UserMixin
# import sqlite3
# from .models import User

# auth = Blueprint('auth', __name__)

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         entered_password = request.form.get('password')

#         conn = sqlite3.connect("instance/database.db")
#         c = conn.cursor()
#         c.execute("SELECT * FROM user WHERE email = ?", (email,))
#         user_record = c.fetchone()
#         user_password = user_record[2] if user_record else None
#         conn.close()
        
#         #user = User.query.filter_by(email=email).first()
#         user = User(user_record[0], user_record[1], user_record[2], user_record[3]) if user_record else None
#         user_password = user.password if user else None
#         if user:
#             if check_password_hash(user_password, entered_password):
#                 flash('Logged in successfully!', category='success')
#                 user.is_authenticated = True
#                 login_user(user, remember=True)
#                 return redirect(url_for('views.calculate_route'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

#     return render_template("login.html", user=current_user)

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   ##means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user

import sqlite3

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                # go to map if login successful
                return redirect(url_for('views.show_map'))
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