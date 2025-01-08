from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#####################################################
# GROUP A Skill : Complex User defined Databases    #
#####################################################
class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(150))
    dest = db.Column(db.String(150))
    distance = db.Column(db.Float)
    time = db.Column(db.Float)
    path_codes = db.Column(db.String(10000))
    path_names = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    routes = db.relationship('Route')
