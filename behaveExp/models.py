from datetime import datetime
from behaveExp import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.Integer)

    name = db.Column(db.String(10))
    value = db.Column(db.Float)
    market = db.Column(db.String(10))
    hold_num = db.Column(db.Float)

    stage = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now, index=True)


class UserValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.Integer)

    value = db.Column(db.Float)
    remain = db.Column(db.Float)

    stage = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now, index=True)


class Time(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now, index=True)

    stage = db.Column(db.Integer)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(10))
    first_round_market = db.Column(db.String(10))
    second_round_market = db.Column(db.String(10))
    third_round_market = db.Column(db.String(10))
    fourth_round_market = db.Column(db.String(10))

    time = db.Column(db.DateTime, default=datetime.now, index=True)


class UserStockDefault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    market = db.Column(db.String(10))
    name = db.Column(db.String(10))

    p_rise = db.Column(db.Float)

    stage = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now, index=True)


class CalculateInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    num_1 = db.Column(db.Integer)
    num_2 = db.Column(db.Integer)
    ans = db.Column(db.Integer)

    stage = db.Column(db.Integer)
    correct = db.Column(db.Integer)
    time = db.Column(db.DateTime, default=datetime.now, index=True)





