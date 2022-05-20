from ai_player import AIPlayer
from copy import deepcopy
import sys


class AIPlayerAlphaBeta(AIPlayer):
    def recursive_function(self, board, depth, symbol):
        return self.alphabeta(board, depth, symbol)

    def alphabeta(self, board, depth, symbol, alpha=-sys.maxsize, beta=sys.maxsize):
        if depth == 0 or self._game.check_winning(board) or self._game.check_draw(board):
            prev_symbol = self._game.get_previous_symbol(symbol)
            # previous symbol is needed because the last call of this function has changed the symbol,
            # but we are calculating heuristics for the same board (without making another move with the changed symbol)
            score = self.heuristic_function(board, prev_symbol)
            if prev_symbol == self._symbol:
                return score
            else:
                return -score

        moves = board.get_free_tiles_with_neighbour()
        if not moves:
            moves = board.get_free_tiles()

        if symbol == self._symbol:  # my turn - maximizing
            value = -sys.maxsize
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = max(value, self.alphabeta(new_board, depth-1, self._game.get_next_symbol(symbol), alpha, beta))

                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value

        else:  # not my turn - minimizing
            value = sys.maxsize
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = min(value, self.alphabeta(new_board, depth-1, self._game.get_next_symbol(symbol), alpha, beta))

                if value <= alpha:
                    break
                beta = min(beta, value)
            return value
