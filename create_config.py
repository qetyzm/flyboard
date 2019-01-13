import os
import json

HOME_DIR = os.path.expanduser('~')
BASE_DIR = os.path.join(HOME_DIR, "flyboard")

if not os.path.isdir(BASE_DIR):
    os.makedirs(BASE_DIR)

DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'flyboard.db')

print("== CREATING CONFIG FILE ==")
SITE_NAME = input("Site name: ")
SECRET_KEY = input("Secret key: ")
CSRF_SESSION_KEY = input("CSRF session key: ")

config = {
    "SITE_NAME": SITE_NAME,
    "DEBUG": True,
    "SQLALCHEMY_DATABASE_URI": DATABASE_URI,
    "SQLALCHEMY_TRACK_MODIFICATIONS": True,
    "SQLALCHEMY_ECHO": True,
    "TESTING": False,
    "THREADS_PER_PAGE": 2,
    "CSRF_ENABLED": True,
    "CSRF_SESSION_KEY": CSRF_SESSION_KEY,
    "SECRET_KEY": SECRET_KEY
}

CONFIG_PATH = os.path.join(BASE_DIR, 'config.json')

with open(CONFIG_PATH, 'w') as f:
    json.dump(config, f, indent=4)

print("\nSaved config to: " + CONFIG_PATH)