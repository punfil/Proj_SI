import constants
import sys


def basic(board, active_player_symbol):
    winner = board.get_winner()
    if winner:
        if winner == active_player_symbol:
            score = sys.maxsize
        else:
            score = -sys.maxsize
    elif board.check_draw():
        score = 100
    else:
        score = 0
    # board.draw()
    # print(score, active_player_symbol)
    return score


def line_length(board, active_player_symbol):
    winner = board.get_winner()
    if winner:
        if winner == active_player_symbol:
            score = sys.maxsize
        else:
            score = -sys.maxsize
    elif board.check_draw():
        score = 100
    else:
        score = 0

    length = constants.required_line_length + 1
    if length > board.width or length > board.height:
        length = constants.required_line_length
    for line in board.iter_lines(length):
        my_symbols = line.count(active_player_symbol)
        other_symbols = sum(1 for symbol in line if symbol is not None and symbol != active_player_symbol)
        score += my_symbols ** 3
        score -= other_symbols ** 2
    # board.draw()
    # print(score, "???", active_player_symbol)
    return score