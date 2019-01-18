from flask import Blueprint, render_template, g, redirect, url_for
from flask_login import login_required
from flyboard.board.models import Board

mod_module = Blueprint('mod', __name__, url_prefix='/mod')

@mod_module.route('/panel', methods=['GET'])
@login_required
def panel():
    return render_template('mod/panel.html')


@mod_module.route('/panel/general_settings', methods=['GET'])
@login_required
def general_settings():
    if g.user.has_permission("flyboard.admin.panel_access"):
        return render_template('mod/general_settings.html')
    else:
        return redirect(url_for('mod.panel'))