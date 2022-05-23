from player import Player
from copy import deepcopy
import sys
import random


class AIPlayer(Player):
    def __init__(self, symbol, game, recursion_depth, heuristic_function):
        super().__init__(symbol, game)

        self._recursion_depth = recursion_depth
        self._heuristic_function = heuristic_function

    def get_move(self):
        x, y = self.decide()
        return x, y

    def is_ready(self):
        return True

    def heuristic_function(self, board, active_player_symbol):
        return self._heuristic_function(board, active_player_symbol)

    def get_possible_moves(self, board):
        moves = board.get_free_tiles_with_neighbour()
        if not moves:
            moves = board.get_free_tiles()
        return moves

    def decide(self):
        moves = self.get_possible_moves(self._game.board)
        evals = [-sys.maxsize for _ in moves]

        for i in range(len(evals)):
            new_board = deepcopy(self._game.board)
            new_board.make_move(moves[i], self._symbol)
            # print(moves[i])
            evals[i] = self.recursive_function(new_board, self._recursion_depth - 1,
                                               self._game.get_next_symbol(self._symbol))
            # print()

        # for i in range(len(evals)):
        #     print(moves[i], '~', evals[i])

        best_eval = max(evals)

        new_moves = []
        for i in range(len(evals)):
            if evals[i] == best_eval:
                new_moves.append(moves[i])

        best_move = random.choice(new_moves)

        return best_move

    def recursive_function(self, board, depth, symbol):
        raise NotImplementedError()

    @property
    def recursion_depth(self):
        return self._recursion_depth

    @recursion_depth.setter
    def recursion_depth(self, value):
        self._recursion_depth = value
