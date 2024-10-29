from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path


db = SQLAlchemy()
DB_NAME = "database.db"
app = Flask(__name__)
login_manager = LoginManager()

def create_app():
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    db.init_app(app)
    
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    with app.app_context():
        db.create_all()

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    return app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
    

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

@app.route('/lines')
def show_lines():
    return render_template('lines.svg')

@app.route('/map')
def calculate_route():
    start = request.args.get('start')
    dest = request.args.get('dest')
