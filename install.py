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
    "LANGUAGE": "en_US"
}

CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=4)

print(config)
print("\nSaved config to: " + CONFIG_PATH)
print('-' * 20)
admin_username = input("Admin username: ")
admin_password = ""
while admin_password == "":
    admin_password = input("Admin password: ")
    if admin_password == "":
        print("*Please enter any password*")

from flyboard import db
from flyboard.auth.models import User

admin = User(username=admin_username, password=admin_password)

db.session.add(admin)
db.session.commit()