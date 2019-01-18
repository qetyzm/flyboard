from flask import Blueprint, render_template, g
from flyboard.board.models import Board

board_module = Blueprint('board', __name__, url_prefix='/board')


@board_module.route('/test')
def test():
    return render_template('board/test.html')


@board_module.route('/<uri>/')
def board_index(uri):
    board = Board.query.filter_by(uri=uri).first()
    if not board:
        return render_template('404.html'), 404
    return render_template('board/board_index.html', board=board)