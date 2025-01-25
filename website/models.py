# from sqlalchemy.sql import func
# from . import db
# from flask_login import UserMixin

#########################################
# GROUP A Skill : Complex Data model    #
#########################################
# class Route(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     start = db.Column(db.String(150))
#     end = db.Column(db.String(150))
#     distance = db.Column(db.Float)
#     time = db.Column(db.Float)
#     path_codes = db.Column(db.String(10000))
#     path_names = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())


# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(150), unique=True)
#     first_name = db.Column(db.String(150))
#     password = db.Column(db.String(150))
#     routes = db.relationship('Route')
#     settings = db.relationship('AccountSettings')
    
# class AccountSettings(db.Model):
#     user = db.relationship('User')
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     preferred_route = db.Column(db.String(150))
#     algorithm = db.Column(db.String(150))

# class Route(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     start = db.Column(db.String(150))
#     end = db.Column(db.String(150))
#     distance = db.Column(db.Float)
#     time = db.Column(db.Float)
#     path_codes = db.Column(db.String(10000))
#     path_names = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())

import sqlite3

#########################################
# GROUP A Skill : Complex Data model    #
#########################################
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
            distance REAL,
            time REAL,
            path_codes TEXT,
            path_names TEXT,
            date TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES user(id)
        )
    """)

    conn.commit()
    conn.close()