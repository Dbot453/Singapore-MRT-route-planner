from flask import Blueprint, render_template, request, redirect, url_for

home = Blueprint('home', __name__)

@home.route('/', methods=['GET', 'POST'])
def home_view():
    """
    Render the home page.
    """
    if request.method == 'POST':
        if 'login' in request.form:
            return redirect(url_for('auth.login'))
        
        elif 'signup' in request.form:
            return redirect(url_for('auth.sign_up'))

    return render_template('home.html', user=None)