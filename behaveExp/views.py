import datetime
import time
from random import random, sample

from flask import jsonify, request, render_template

from behaveExp import app, db
from behaveExp.models import Stock, User, Time, UserStockDefault, UserValue


def random_update(value, p):
    flag = random()
    if flag < p:
        ret = value * 1.05
    else:
        ret = value * 0.95
    return ret


def random_market():
    flag = random()
    if flag < 0.5:
        return "A"
    else:
        return "B"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    userName = data["userName"]

    user = User(
        user_name=userName,
        first_round_market=random_market(),
        second_round_market=random_market()
    )
    db.session.add(user)
    db.session.commit()

    current_user = User.query.filter_by(user_name=userName).first()
    user_id = current_user.id
    db.session.add(
        UserValue(
            user_id=user_id,
            date=0,
            value=1000,
            remain=1000
        )
    )

    p_rise_A = sample([0.45, 0.5, 0.55], 3)
    p_rise_B = sample([0.45, 0.5, 0.55], 3)
    stock_names = ["A", "B", "C"]

    for i in range(3):
        db.session.add(
            UserStockDefault(
                user_id=user_id,
                market="A",
                name=stock_names[i],
                p_rise=p_rise_A[i]
            )
        )

        db.session.add(
            UserStockDefault(
                user_id=user_id,
                market="B",
                name=stock_names[i],
                p_rise=p_rise_B[i]
            )
        )

        db.session.add(
            Stock(
                user_id=user_id,
                date=0,
                name=stock_names[i],
                value=100,
                market="A",
                hold_num=0
            )
        )

        db.session.add(
            Stock(
                user_id=user_id,
                date=0,
                name=stock_names[i],
                value=100,
                market="B",
                hold_num=0
            )
        )

    db.session.commit()
    return 'done'


@app.route('/get_stock_info', methods=['POST'])
def get_stock_info():
    data = request.get_json()

    user_name = data['userName']
    nround = int(data['nround'])
    ratio = data['ratio']
    ratio_2 = data['ratio_2']
    ratio_3 = data['ratio_3']
    remain = data['remain']

    current_user = User.query.filter_by(user_name=user_name).first()
    current_user_value = UserValue.query.filter(
        UserValue.user_id == current_user.id,
        UserValue.date == nround - 1).first()
    current_stock = Stock.query.filter(
        Stock.user_id == current_user.id,
        Stock.date == nround - 1
    ).order_by(
        Stock.market,
        Stock.name
    ).all()

    default_p = UserStockDefault.query.filter(
        UserStockDefault.user_id == current_user.id
    ).order_by(
        UserStockDefault.market,
        UserStockDefault.name
    )

    market = current_user.first_round_market
    if market == "A":
        new_hold = [
            (current_user_value.value * ratio / 100) / current_stock[0].value,
            (current_user_value.value * ratio_2 / 100) / current_stock[1].value,
            (current_user_value.value * ratio_3 / 100) / current_stock[2].value,
            0, 0, 0
        ]
    else:
        new_hold = [
            0, 0, 0,
            (current_user_value.value * ratio / 100) / current_stock[3].value,
            (current_user_value.value * ratio_2 / 100) / current_stock[4].value,
            (current_user_value.value * ratio_3 / 100) / current_stock[5].value
        ]

    new_all_value = 0
    for i in range(6):
        stock = current_stock[i]
        default = default_p[i]
        new_value = random_update(stock.value, default.p_rise)
        hold_num = new_hold[i]
        db.session.add(
            Stock(
                user_id=current_user.id,
                date=nround,
                name=stock.name,
                value=new_value,
                market=stock.market,
                hold_num=hold_num
            )
        )
        new_all_value = new_all_value + hold_num * new_value
    new_remain = current_user_value.value * remain / 100
    db.session.add(
        UserValue(
            user_id=current_user.id,
            date=nround,
            value=new_all_value + new_remain,
            remain=new_remain
        )
    )

    db.session.commit()
    return "ok"


@app.route('/get_user_info', methods=['GET', 'POST'])
def get_user_info():
    current_date = int(request.args.get('nround'))
    user_name = str(request.args.get('userName'))
    current_user = User.query.filter(User.user_name == user_name).first()
    while not current_user:
        current_user = User.query.filter(User.user_name == user_name).first()
    user_market = current_user.first_round_market

    user_stock = Stock.query.filter(
        Stock.user_id == current_user.id,
        Stock.date == current_date - 1,
        Stock.market == user_market
    ).order_by(
        Stock.name
    ).all()
    while not user_stock:
        user_stock = Stock.query.filter(
            Stock.user_id == current_user.id,
            Stock.date == current_date - 1,
            Stock.market == user_market
        ).order_by(
            Stock.name
        ).all()

    user_value = UserValue.query.filter(
        UserValue.user_id == current_user.id,
        UserValue.date == current_date - 1
    ).first()
    while not user_value:
        user_value = UserValue.query.filter(
            UserValue.user_id == current_user.id,
            UserValue.date == current_date - 1
        ).first()

    user_total_value = user_value.value
    ratio_list = []
    for i in range(3):
        stock = user_stock[i]
        ratio_i = stock.hold_num * stock.value / user_total_value
        ratio_i = int(round(ratio_i, 2) * 100)
        ratio_list.append(
            ratio_i
        )

    data = {
        'stock_name': "A",
        'stock_ratio': ratio_list[0],
        'stock_name_2': "B",
        'stock_ratio_2': ratio_list[1],
        'stock_name_3': "C",
        'stock_ratio_3': ratio_list[2]
    }

    return jsonify(data)


@app.route('/get_figure', methods=['GET'])
def get_figure():
    user_name = str(request.args.get('id'))

    current_user = User.query.filter_by(user_name=user_name).first()
    stocks = Stock.query.filter(
        Stock.user_id == current_user.id
    )

    stock_A = stocks.filter(
        Stock.market == "A"
    ).order_by(
        Stock.date,
        Stock.name
    ).all()

    i = 0
    data_A = []
    data_B = []
    data_C = []
    while i < len(stock_A):
        data_A.append(round(stock_A[i].value, 2))
        i = i + 1
        data_B.append(round(stock_A[i].value, 2))
        i = i + 1
        data_C.append(round(stock_A[i].value, 2))
        i = i + 1

    days = ["Day" + str(i) for i in range(int(len(stock_A) / 3))]

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
    option["title"]["text"] = "市场A"
    option["xAxis"]["data"] = days
    option["series"][0]["data"] = data_A
    option["series"][1]["data"] = data_B
    option["series"][2]["data"] = data_C

    stock_B = stocks.filter(
        Stock.market == "B"
    ).order_by(
        Stock.date,
        Stock.name
    ).all()

    i = 0
    data_A = []
    data_B = []
    data_C = []
    while i < len(stock_B):
        data_A.append(round(stock_B[i].value, 2))
        i = i + 1
        data_B.append(round(stock_B[i].value, 2))
        i = i + 1
        data_C.append(round(stock_B[i].value, 2))
        i = i + 1

    days = ["Day" + str(i) for i in range(int(len(stock_B) / 3))]

    option_B = {
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
    option_B["title"]["text"] = "市场B"
    option_B["xAxis"]["data"] = days
    option_B["series"][0]["data"] = data_A
    option_B["series"][1]["data"] = data_B
    option_B["series"][2]["data"] = data_C

    return jsonify({
        'op1': option,
        'op2': option_B
    })


@app.route('/get_reward', methods=['GET'])
def get_reward():
    user_name = str(request.args.get('id'))
    nround = int(request.args.get('nround'))

    current_user = User.query.filter_by(user_name=user_name).first()
    current_user_value = UserValue.query.filter(
        UserValue.user_id == current_user.id,
        UserValue.date == nround
    ).first()
    last_user_value = UserValue.query.filter(
        UserValue.user_id == current_user.id,
        UserValue.date == nround - 1
    ).first()

    total_value = current_user_value.value
    current_reward = current_user_value.value - last_user_value.value
    total_reward = total_value - 1000

    return jsonify(
        {
            "total_value": round(total_value, 2),
            "current_reward": round(current_reward, 2),
            "total_reward": round(total_reward, 2)
        }
    )


@app.route('/market_info', methods=['GET'])
def market_info():
    current_date = int(request.args.get('nround'))
    user_name = str(request.args.get('id'))
    current_user = User.query.filter(User.user_name == user_name).first()

    market = random_market()

    stocks = Stock.query.filter(
        Stock.market == market,
        Stock.user_id == current_user.id
    )
    while len(stocks.all()) != current_date * 3 + 3:
        stocks = Stock.query.filter(
            Stock.market == market,
            Stock.user_id == current_user.id
        )

    ori_stock = stocks.filter(
        Stock.date == 0
    ).all()

    ori_value = sum([stock.value for stock in ori_stock])
    current_stock = stocks.filter(
        Stock.date == current_date
    ).all()

    current_value = sum([stock.value for stock in current_stock])
    current_index = (current_value / ori_value) * 1000

    if current_date == 1:
        last_index = 1000
    else:
        last_stock = stocks.filter(
            Stock.date == current_date - 1
        ).all()
        last_value = sum([stock.value for stock in last_stock])
        last_index = (last_value / ori_value) * 1000

    value_diff = round(current_index - last_index, 2)

    if value_diff < 0:
        value_diff = "下降" + str(-value_diff) + "点"
    else:
        value_diff = "上升" + str(value_diff) + "点"

    return jsonify(
        {
            "current_index": round(current_index, 2),
            "value_diff": value_diff
        }
    )


@app.route('/post_time', methods=['POST'])
def post_time():
    data = request.get_json()
    user_name = data["userName"]
    current_user = User.query.filter_by(user_name=user_name).first()
    while not current_user:
        current_user = User.query.filter_by(user_name=user_name).first()
    current_time = Time.query.filter(
        Time.user_id == current_user.id
    ).first()

    if not current_time:
        db.session.add(Time(user_id=current_user.id))
        db.session.commit()
    return 'ok'


@app.route('/get_time', methods=['GET', 'POST'])
def get_time():
    current_time = datetime.datetime.now()
    user_name = request.args.get("userName")
    current_user = User.query.filter_by(user_name=user_name).first()
    while not current_user:
        current_user = User.query.filter_by(user_name=user_name).first()
    start_time = Time.query.filter(
        Time.user_id == current_user.id
    ).first()

    if not start_time:
        return jsonify(
            {
                'sec': 0,
                'mint': 0
            }
        )
    else:
        start_time = start_time.time

    last_second = (current_time - start_time).seconds

    sec = last_second % 60
    mint = int(last_second / 60)

    return jsonify(
        {
            'sec': sec,
            'mint': mint
        }
    )
