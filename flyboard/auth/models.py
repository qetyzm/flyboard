from flyboard import db, Base
from werkzeug.security import generate_password_hash, check_password_hash

from flyboard.board.models import Board

controlled_boards = db.Table(
    'controlled_boards',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('board_id', db.Integer, db.ForeignKey('board.id'), primary_key=True)
)
    
role_permissions = db.Table(
    'role_permissions',
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True),
    db.Column('role_permission_id', db.Integer, db.ForeignKey('role_permission.id'), primary_key=True)
)


class Role(Base):
    __tablename__ = 'role'
    name = db.Column(db.String(200), nullable=False, unique=True)
    permissions = db.relationship('RolePermission', secondary=role_permissions,
                                  lazy='subquery',
                                  backref=db.backref('roles', lazy=True))
    users = db.relationship('User', backref='role', lazy=True)

    def __init__(self, name):
        self.name = name
        self.permissions = []


class RolePermission(Base):
    __tablename__ = 'role_permission'
    key = db.Column(db.String(200), nullable=False, unique=True)

    def __init__(self, key):
        self.key = key


class User(Base):
    __tablename__ = 'user'
    username = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    boards = db.relationship('Board', secondary=controlled_boards, 
                             lazy='subquery', 
                             backref=db.backref('owners', lazy=True))

    def __init__(self, username, password, role):
        self.username = username
        self.set_password(password)
        self.role = role
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

    def has_permission(self, permission):
        if not self.role:
            return False
        levels = permission.split('.')
        for permission in self.role.permissions:
            perm_levels = permission.key.split('.')
            for i in range(min(len(levels), len(perm_levels))):
                is_last_level = (i == min(len(levels), len(perm_levels)) - 1)
                if perm_levels[i] == "*":
                    return True
                elif perm_levels[i] != levels[i]:
                    break
                elif is_last_level and perm_levels[i] == levels[i]:
                    return True
        return False