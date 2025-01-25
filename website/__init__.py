from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
import sqlite3
from .models import init_db


db = SQLAlchemy()
DB_NAME = "database.db"
app = Flask(__name__)
login_manager = LoginManager()

def create_app():
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    init_db()
    
    from .views import views
    from .auth import auth
    from .map import map
    from .home import home
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(map, url_prefix='/')
    app.register_blueprint(home, url_prefix='/')
    

    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)


    @login_manager.user_loader
    def load_user(user_id):
        conn = sqlite3.connect("instance/database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM user WHERE id = ?", (user_id,))
        user = c.fetchone()
        conn.close()
        return user
    
    return app 

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

