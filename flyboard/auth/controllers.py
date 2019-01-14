from flask import Blueprint, request, render_template,\
                  flash, session, redirect, url_for
from flask_login import login_user, current_user, login_required

from flyboard import app, db, login_manager
from flyboard.auth.forms import LoginForm
from flyboard.auth.models import User

auth_module = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth_module.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')