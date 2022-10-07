from datetime import datetime
from behaveExp import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    value = db.Column(db.Float)
    date = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    n_A = db.Column(db.Float)
    n_B = db.Column(db.Float)
    n_C = db.Column(db.Float)
    remain = db.Column(db.Float)
    date = db.Column(db.Integer)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now, index=True)
