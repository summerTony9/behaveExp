import json
from random import random

from flask import jsonify, request

from behaveExp import app, db
from behaveExp.models import Stock, User


def random_update(value, p):
    flag = random()
    if flag < p:
        ret = value * 1.05
    else:
        ret = value * 0.95
    return ret


@app.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    all_stock = Stock.query.all()
    current_date = max([stock.date for stock in all_stock])
    current_stock = Stock.query.filter_by(date=current_date).all()

    current_value = [stock.value for stock in current_stock]

    new_value = [0, 0, 0]
    for i in range(3):
        new_value[i] = random_update(current_value[i], 0.5)

    db.session.add(Stock(name='A', value=new_value[0], date=current_date + 1))
    db.session.add(Stock(name='B', value=new_value[1], date=current_date + 1))
    db.session.add(Stock(name='C', value=new_value[2], date=current_date + 1))

    current_date = max([user.date for user in User.query.all()])
    current_user = User.query.filter_by(date=current_date).first()

    user_value = current_user.value

    data = request.get_json()

    new_n_A = user_value * (data['ratio'] / 100) / current_value[0]
    new_n_B = user_value * (data['ratio_2'] / 100) / current_value[1]
    new_n_C = user_value * (data['ratio_3'] / 100) / current_value[2]
    new_remain = user_value * (data['remain'] / 100)

    user_value = (
            new_value[0] * new_n_A +
            new_value[1] * new_n_B +
            new_value[2] * new_n_C +
            new_remain
    )

    db.session.add(
        User(
            value=user_value,
            n_A=new_n_A,
            n_B=new_n_B,
            n_C=new_n_C,
            remain=new_remain,
            date=current_date + 1
        )
    )

    db.session.commit()
    return "ok", 200


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    current_date = max([user.date for user in User.query.all()])
    current_user = User.query.filter_by(date=current_date).first()

    all_stock = Stock.query.all()
    current_date = max([stock.date for stock in all_stock])
    current_stock = Stock.query.filter_by(date=current_date).all()
    user_value = current_user.value
    # user_value = (
    #         current_stock[0].value * current_user.n_A +
    #         current_stock[1].value * current_user.n_B +
    #         current_stock[2].value * current_user.n_C +
    #         current_user.remain
    # )

    ratio_A = current_stock[0].value * current_user.n_A / user_value
    ratio_B = current_stock[1].value * current_user.n_B / user_value
    ratio_C = current_stock[2].value * current_user.n_C / user_value

    data = {
        'stock_name': "A",
        'stock_ratio': int(round(ratio_A, 2) * 100),
        'stock_name_2': "B",
        'stock_ratio_2': int(round(ratio_B, 2) * 100),
        'stock_name_3': "C",
        'stock_ratio_3': int(round(ratio_C, 2) * 100)
    }

    return jsonify(data)


@app.route('/get_figure', methods=['GET'])
def get_figure():
    all_stock = Stock.query.all()
    days = ["Day" + str(i) for i in range(int(len(all_stock)/3))]
    i = 0
    data_A = []
    data_B = []
    data_C = []
    while i < len(all_stock):
        data_A.append(all_stock[i].value)
        i = i + 1
        data_B.append(all_stock[i].value)
        i = i + 1
        data_C.append(all_stock[i].value)
        i = i + 1

    option = {
        "title": {
            "text": '市场A'
        },
        "tooltip": {
            "trigger": 'axis'
        },
        "legend": {
            "data": ['A', 'B', 'C']
        },
        "grid": {
            "left": '3%',
            "right": '4%',
            "bottom": '3%',
            "containLabel": "true"
        },
        "toolbox": {
            "feature": {
                "saveAsImage": {}
            }
        },
        "xAxis": {
            "type": 'category',
            "boundaryGap": "false",
            "data": ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        },
        "yAxis": {
            "type": 'value'
        },
        "series": [
            {
                "name": 'A',
                "type": 'line',
                "data": [120, 132, 101, 134, 90, 230, 210]
            },
            {
                "name": 'B',
                "type": 'line',
                "data": [220, 182, 191, 234, 290, 330, 310]
            },
            {
                "name": 'C',
                "type": 'line',
                "data": [150, 232, 201, 154, 190, 330, 410]
            }
        ]
    }

    option["xAxis"]["data"] = days
    option["series"][0]["data"] = data_A
    option["series"][1]["data"] = data_B
    option["series"][2]["data"] = data_C

    return jsonify(option)


@app.route('/get_reward', methods=['GET'])
def get_reward():
    current_date = max([user.date for user in User.query.all()])
    current_user = User.query.filter_by(date=current_date).first()
    last_user = User.query.filter_by(date=current_date-1).first()

    total_value = current_user.value
    current_reward = current_user.value - last_user.value
    total_reward = total_value - 1000

    return jsonify(
        {
            "total_value": round(total_value, 2),
            "current_reward": round(current_reward, 2),
            "total_reward": round(total_reward, 2)
        }
    )




