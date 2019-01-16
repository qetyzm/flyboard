import os
import json

HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.join(HOME_DIR, "flyboard")

import shutil
try:
    shutil.rmtree(BASE_DIR)
except:
    pass

if not os.path.isdir(BASE_DIR):
    os.makedirs(BASE_DIR)

DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'flyboard.db')

print("== CREATING CONFIG FILE ==")
SITE_NAME = input("Site name: ")
SECRET_KEY = input("Secret key: ")
CSRF_SESSION_KEY = input("CSRF session key: ")
RECAPTCHA_API_KEY = input("ReCatpcha API key (don't enter anything if you don't want reCaptcha): ")

config = {
    "SITE_NAME": SITE_NAME,
    "RECAPTCHA_API_KEY": RECAPTCHA_API_KEY,
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": DATABASE_URI,
    "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    "SQLALCHEMY_ECHO": True,
    "TESTING": False,
    "THREADS_PER_PAGE": 2,
    "CSRF_ENABLED": True,
    "CSRF_SESSION_KEY": CSRF_SESSION_KEY,
    "SECRET_KEY": SECRET_KEY,
    "LANGUAGE": "en_US",
    "ANNOUNCEMENT": "",
    "DEFAULT_BOARD_LIST": "b",
    "SESSION_TIME_ONLINE_MINUTES": 5
}

CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=4)

print(config)
print("\nSaved config to: " + CONFIG_PATH)
print('-' * 20)

## Create permissions
from flyboard.auth.models import RolePermission
from flyboard import db

perms = (
    RolePermission(key="*"),
    RolePermission(key="flyboard.*"),
    RolePermission(key="flyboard.admin.*"),
    RolePermission(key="flyboard.admin.panel_access"),
    RolePermission(key="flyboard.admin.set_perms"),
    RolePermission(key="flyboard.admin.signature"),
    RolePermission(key="flyboard.mod.*"),
    RolePermission(key="flyboard.mod.panel_access"),
    RolePermission(key="flyboard.mod.signature"),
    RolePermission(key="flyboard.posts.*"),
    RolePermission(key="flyboard.posts.ban"),
    RolePermission(key="flyboard.posts.delete"),
    RolePermission(key="flyboard.posts.move"),
    RolePermission(key="flyboard.posts.shadowmute"),
    RolePermission(key="flyboard.posts.show_ip"),
    RolePermission(key="flyboard.user.*"),
    RolePermission(key="flyboard.user.create"),
    RolePermission(key="flyboard.user.delete"),
    RolePermission(key="flyboard.vip.*"),
    RolePermission(key="flyboard.vip.signature")
)

for perm in perms:
    db.session.add(perm)

## Create roles

from flyboard.auth.models import Role

role_moderator = Role(name="Mod")
role_moderator.permissions.append(RolePermission.query.filter_by(key="flyboard.mod.*").first())
role_moderator.permissions.append(RolePermission.query.filter_by(key="flyboard.posts.*").first())


role_admin = Role(name="Admin")
role_admin.permissions.append(RolePermission.query.filter_by(key="flyboard.admin.*").first())
role_admin.permissions.append(RolePermission.query.filter_by(key="flyboard.posts.*").first())

role_vip = Role(name="VIP")
role_vip.permissions.append(RolePermission.query.filter_by(key="flyboard.vip.*").first())

db.session.add(role_moderator)
db.session.add(role_admin)
db.session.add(role_vip)

## Create admin
admin_username = input("Admin username: ")
admin_password = ""
while admin_password == "":
    admin_password = input("Admin password: ")
    if admin_password == "":
        print("*Please enter any password*")

from flyboard.auth.models import User

admin = User(username=admin_username, password=admin_password, role=role_admin)

db.session.add(admin)

## Create board /b/
from flyboard.board.models import Board
"""
board_a = Board(
    uri="a", 
    title="Anime", 
    ids_allowed=True, 
    mute_videos=False)
"""
board_b = Board(
    uri="b", 
    title="Random", 
    ids_allowed=True, 
    mute_videos=False)
"""
board_c = Board(
    uri="c", 
    title="Technology", 
    ids_allowed=True, 
    mute_videos=False)
"""

#db.session.add(board_a)
db.session.add(board_b)
#db.session.add(board_c)
db.session.commit()