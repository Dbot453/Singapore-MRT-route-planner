from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        entered_password = request.form.get('password')

        new_user = User.query.filter_by(email=email).first()
        user_password = new_user.password if new_user else None
        if new_user:
            if check_password_hash(user_password, entered_password):
                flash('Logged in successfully!', category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('map.calculate_route'))
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

        user = User.query.filter_by(email=email).first()
        if password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            if user:
                flash('Email already exists.', category='error')
            else:
                new_user = User(email=email, first_name=first_name, password=password1)
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!', category='success')
                return redirect(url_for('auth.login'))

    return render_template("sign_up.html", user=current_user)