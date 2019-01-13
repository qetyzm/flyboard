from flask import Blueprint, render_template, g

board_module = Blueprint('board', __name__, url_prefix='/board')


@board_module.route('/test')
def test():
    return render_template('board/test.html')