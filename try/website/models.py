from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data =  db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    full_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    age = db.Column(db.String(150))
    country = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    nick_name = db.Column(db.String(150), unique=True)
    friends = db.Column(db.String(150))
    pending_requests = db.Column(db.String(150))
    sended_requests = db.Column(db.String(150))
    image = db.Column(db.String(150))
    github = db.Column(db.String(150))
    discord = db.Column(db.String(150))


    # ------ > Games User is playing.
    league_player = db.Column(db.Boolean, default=False, nullable=False)
    fortnite_player = db.Column(db.Boolean, default=False, nullable=False)
    cs_player = db.Column(db.Boolean, default=False, nullable=False)
    minecraft_player = db.Column(db.Boolean, default=False, nullable=False)
    cod_player = db.Column(db.Boolean, default=False, nullable=False)
    r6_player = db.Column(db.Boolean, default=False, nullable=False)