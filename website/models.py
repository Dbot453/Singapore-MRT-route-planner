from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#########################################
# GROUP A Skill : Complex Data model    #
#########################################
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start = db.Column(db.String(150))
    end = db.Column(db.String(150))
    distance = db.Column(db.Float)
    time = db.Column(db.Float)
    path_codes = db.Column(db.String(10000))
    path_names = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    routes = db.relationship('Route')
    settings = db.relationship('AccountSettings')
    
class AccountSettings(db.Model):
    user = db.relationship('User')
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    preferred_route = db.Column(db.String(150))
    algorithm = db.Column(db.String(150))

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start = db.Column(db.String(150))
    end = db.Column(db.String(150))
    distance = db.Column(db.Float)
    time = db.Column(db.Float)
    path_codes = db.Column(db.String(10000))
    path_names = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())