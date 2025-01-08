from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user
from . import db

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('auth.login'))
        
        elif 'signup' in request.form:
            return redirect(url_for('auth.sign_up'))
    return render_template('home.html')
5