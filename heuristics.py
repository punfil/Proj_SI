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


def better_line_length(board, active_player_symbol):
    score = basic(board, active_player_symbol)
    if score == sys.maxsize:
        return score - len(board.get_occupied_tiles())
    elif score == -sys.maxsize:
        return score + len(board.get_occupied_tiles())

    length = constants.required_line_length
    # if length > board.width or length > board.height:
    #    length = constants.required_line_length
    for line in board.iter_lines(length):
        my_symbols_max = 0
        my_symbols = 0
        other_symbols_max = 0
        other_symbols = 0
        for symbol in line:
            if symbol == active_player_symbol:
                my_symbols += 1
                if my_symbols == constants.required_line_length:
                    return sys.maxsize - len(board.get_occupied_tiles())
                if other_symbols > other_symbols_max:
                    other_symbols_max = other_symbols
                other_symbols = 0
            else:
                if symbol is not None:
                    other_symbols += 1
                    if my_symbols > my_symbols_max:
                        my_symbols_max = my_symbols
                    my_symbols = 0

        if my_symbols > my_symbols_max:
            my_symbols_max = my_symbols
        if other_symbols > other_symbols_max:
            other_symbols_max = other_symbols

        score += (my_symbols_max ** 3) // 8
        score -= (other_symbols_max ** 3) // 8
    # board.draw()
    # print(score, "???", active_player_symbol)
    return score


def num_tiles_test(board, active_player_symbol):
    score = len(board.get_occupied_tiles())
    return score


def line_length_turn_number(board, active_player_symbol):
    score = line_length(board, active_player_symbol)

    occupied_tiles = board.get_occupied_tiles()  # the number of occupied tiles = how many turns have been made
    score -= len(occupied_tiles) * 10  # we want to end games fast, so decrease score for every turn

    return score
