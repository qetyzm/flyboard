from flyboard import db, Base
from werkzeug.security import generate_password_hash, check_password_hash

from flyboard.board.models import Board

controlled_boards = db.Table(
    'controlled_boards',
    db.Column(
        'user_id',
        db.Integer, 
        db.ForeignKey('user.id'), 
        primary_key=True),
    db.Column(
        'board_id',
        db.Integer, 
        db.ForeignKey('board.id'), 
        primary_key=True)
)


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    boards = db.relationship('Board', secondary=controlled_boards)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
        self.perms = 0
        self.active = True
        self.boards = []

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)