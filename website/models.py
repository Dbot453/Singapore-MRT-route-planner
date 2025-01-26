from sqlalchemy.sql import func
from . import db
from flask_login import UserMixin
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))

    # what these for?
    #routes = db.relationship('Route')
    #settings = db.relationship('AccountSettings')
    
    def __init__(self, id, email,  password, first_name):
        self.id = id 
        self.email = email
        self.password = password
        self.first_name = first_name

    def __repr__(self):
        return '<User %r>' % self.email

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.email)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
    
#########################################
# GROUP A Skill : Complex Data model    #
#########################################
def init_db():
    conn = sqlite3.connect("website/database.db")
    c = conn.cursor()
    # Table for user
    c.execute("""
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            first_name TEXT,
            password TEXT
        )
    """)
    # Table for account settings
    c.execute("""
        CREATE TABLE IF NOT EXISTS account_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            preferred_route TEXT,
            algorithm TEXT,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """)
    # Table for route
    c.execute("""
        CREATE TABLE IF NOT EXISTS route (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            start TEXT,
            end TEXT,
            distance NUMERIC,
            travel_time NUMERIC,
            path_codes TEXT,
            path_names TEXT,
            SAVE_datetime datetime DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER,
            preferred_route TEXT,
            algorith_selection TEXT,
        )
    """)

    conn.commit()
    conn.close()