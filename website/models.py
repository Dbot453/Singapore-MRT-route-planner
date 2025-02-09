from sqlalchemy.sql import func
from . import db
from flask_login import UserMixin
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

#########################################
# GROUP A Skill : Complex Data model    #
#########################################

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relationships
    # account_settings = db.relationship('AccountSettings', backref='user', lazy=True)
    # routes = db.relationship('Route', backref='user', lazy=True)
    
    def __init__(self, email, password, first_name):
        self.email = email
        self.set_password(password)
        self.first_name = first_name

    def __repr__(self):
        return '<User %r>' % self.email

    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def check_active(self):
        return True
    
def init_db():
    conn = sqlite3.connect("instance/database.db")
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
            age INTEGER,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """)
    try:
        c.execute("ALTER TABLE account_settings ADD COLUMN age INTEGER")
    except sqlite3.OperationalError as e:
        if "duplicate column" not in str(e):
            raise
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
            algorith_selection TEXT
        )
    """)

    conn.commit()
    conn.close()
    