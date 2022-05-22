import constants
import sys


def basic(board, active_player_symbol):
    winner = board.get_winner()
    if winner:
        if winner == active_player_symbol:
            score = sys.maxsize
        else:
            score = -sys.maxsize
    else:
        score = 0
    # board.draw()
    # print(score, active_player_symbol)
    return score


def line_length(board, active_player_symbol):
    score = basic(board, active_player_symbol)
    if score == sys.maxsize or score == -sys.maxsize:
        return score

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


def line_length_turn_number(board, active_player_symbol):
    score = line_length(board, active_player_symbol)

    occupied_tiles = board.get_occupied_tiles()  # the number of occupied tiles = how many turns have been made
    score -= len(occupied_tiles) * 10  # we want to end games fast, so decrease score for every turn

    return score
