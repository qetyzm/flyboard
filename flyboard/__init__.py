import os

from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'flyboard', 'config.json')

app = Flask(__name__)
app.config.from_json(CONFIG_PATH)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

@app.before_request
def before_request():
    g.site_name = app.config['SITE_NAME']
    g.user = current_user

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from flyboard.auth.controllers import auth_module
from flyboard.board.controllers import board_module

app.register_blueprint(auth_module)
app.register_blueprint(board_module)

db.create_all()