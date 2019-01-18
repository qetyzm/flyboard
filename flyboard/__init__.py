import os
import random
import json
import time

from flask import Flask, render_template, g, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

CONFIG_PATH = os.path.join(os.path.expanduser('~'), 'flyboard', 'config.json')
MESSAGES_PATH = os.path.join('flyboard', 'messages')

app = Flask(__name__)
app.config.from_json(CONFIG_PATH)
app.config['ONLINE_SESSIONS'] = {}
app.static_path = app.static_folder

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'home'

def load_messages():
    lang = app.config['LANGUAGE']
    with open(os.path.join(MESSAGES_PATH, lang + '.json')) as f:
        return json.loads(f.read())

messages = load_messages()

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

def global_announcement():
    return "The global announcement."

from flyboard.board.models import Board

@app.before_request
def before_request():
    make_session_online()
    g.site_name = app.config['SITE_NAME']
    g.user = current_user
    g.banner = random_banner()
    g.global_announcement = global_announcement()
    g.messages = messages
    g.board_categories = board_categories()
    g.sessions_online = get_sessions_online()


def make_session_online():
    seconds_end_time = 60 * app.config['SESSION_TIME_ONLINE_MINUTES']
    session_end_time = time.time() + seconds_end_time
    app.config['ONLINE_SESSIONS'][request.remote_addr] = session_end_time


def get_sessions_online():
    sessions = app.config['ONLINE_SESSIONS']
    sessions_online = {k: v for k,v in sessions.items() if v > time.time()}
    return len(sessions_online)
        

def board_categories():
    default_board_list = app.config['DEFAULT_BOARD_LIST']
    category_list = default_board_list.replace(' ', '').split('|')
    board_groups = list(map(lambda x: x.split(','), category_list))
    all_boards = Board.query.all()
    uris = list(map(lambda b: b.uri, all_boards))
    board_categories = []
    for board_group in board_groups:
        boards = []
        for uri in board_group:
            if uri in uris:
                board = Board.query.filter_by(uri=uri).first()
                boards.append(board)
        board_categories.append(boards)
    return board_categories 


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


def random_banner():
    banners_path = os.path.join('flyboard', 'static', 'assets', 'banners')
    files = []
    for file in os.listdir(banners_path):
        extensions = (".png", ".jpg", ".gif")
        print(file[-4:])
        if file[-4:] in extensions:
            files.append(file)
    return random.choice(files)


@app.route('/')
def home():
    return render_template('home.html', banner=random_banner())


from flyboard.auth.controllers import auth_module
from flyboard.board.controllers import board_module
from flyboard.mod.controllers import mod_module

app.register_blueprint(auth_module)
app.register_blueprint(board_module)
app.register_blueprint(mod_module)

db.create_all()