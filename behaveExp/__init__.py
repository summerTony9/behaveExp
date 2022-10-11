from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        variable_start_string='%%',
        variable_end_string='%%',
    ))


app = CustomFlask('behaveExp', template_folder='templates/dist', static_folder='templates/dist/assets')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
CORS(app)
Admin(app, name='microblog', template_mode='bootstrap2')
from behaveExp import views, commands
