from flask import Blueprint, request, render_template,\
                  flash, session, redirect, url_for,\
                  jsonify, g
from flask_login import login_user, current_user, login_required, logout_user

from flyboard import app, db, login_manager
from flyboard.auth.forms import LoginForm
from flyboard.auth.models import User

auth_module = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth_module.route('/login', methods=['POST'])
def login():
    if not request.json:
        return jsonify({"valid": False, "message": g.messages["wrong_content"]})

    username = request.json['username']
    password = request.json['password']

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        login_user(user)
        return jsonify({"valid": True, "message": g.messages["logged_in_successfully"]})
    return jsonify({"valid": False, "message": g.messages["wrong_credentials"]})


@auth_module.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return jsonify({"valid": True, "message": g.messages["logged_out_successfully"]})