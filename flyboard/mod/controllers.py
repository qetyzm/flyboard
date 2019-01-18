from flask import Blueprint, render_template, g
from flyboard.board.models import Board

mod_module = Blueprint('mod', __name__, url_prefix='/mod')

@mod_module.route('/panel')
def board_index(uri):
    return render_template('mod/panel.html')