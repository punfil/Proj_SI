from ai_player import AIPlayer
from copy import deepcopy
import sys


class AIPlayerMinMax(AIPlayer):
    def recursive_function(self, board, depth, symbol):
        return self.minmax(board, depth, symbol)

    def minmax(self, board, depth, symbol):
        if depth == 0 or board.get_winner() or board.check_draw():
            prev_symbol = self._game.get_previous_symbol(symbol)
            # previous symbol is needed because the last call of this function has changed the symbol,
            # but we are calculating heuristics for the same board (without making another move with the changed symbol)
            score = self.heuristic_function(board, prev_symbol)
            if prev_symbol == self._symbol:
                return score
            else:
                return -score

        moves = self.get_possible_moves(board)

        if symbol == self._symbol:  # my turn - maximizing
            value = -sys.maxsize
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = max(value, self.minmax(new_board, depth - 1, self._game.get_next_symbol(symbol)))
            return value

        else:  # not my turn - minimizing
            value = sys.maxsize
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = min(value, self.minmax(new_board, depth - 1, self._game.get_next_symbol(symbol)))
            return value
