from player import Player
from copy import deepcopy
import random


class AIPlayer(Player):
    def __init__(self, symbol, game, recursion_depth):
        super().__init__(symbol, game)

        self.recursion_depth = recursion_depth

    def get_move(self):
        x, y = self.decide()
        return x, y

    def heuristic_function(self, board, active_player_symbol):
        # kinda works, but mostly doesn't, todo
        winner = self._game.check_winning(board)
        if winner:
            if winner == active_player_symbol:
                return 10000
            else:
                return -10000
        elif self._game.check_draw(board):
            return 100
        else:
            return 0

    def decide(self):

        moves = self._game.board.get_free_tiles()
        evals = [-99999 for _ in moves]  # todo

        for i in range(len(evals)):
            new_board = deepcopy(self._game.board)
            new_board.make_move(moves[i], self._symbol)
            new_board.draw()
            evals[i] = self.minmax(new_board, self.recursion_depth - 1, 'o' if self._symbol == 'x' else 'x')
            print(evals[i], '\n\n\n')

        for i in range(len(evals)):
            print(moves[i], '~', evals[i])

        best_eval = max(evals)

        new_moves = []
        for i in range(len(evals)):
            if evals[i] == best_eval:
                new_moves.append(moves[i])
        print('be', best_eval, new_moves)

        best_move = random.choice(new_moves)

        return best_move

    def minmax(self, board, depth, symbol):

        if depth == 0 or self._game.check_winning() or self._game.check_draw():
            return self.heuristic_function(board, symbol)

        moves = board.get_free_tiles()

        if symbol == self._symbol:  # my turn - maximizing
            value = -99999
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = max(value, self.minmax(new_board, depth - 1, 'x'))  # todo I don't like the hardcoded 'x'
            return value

        else:  # not my turn - minimizing
            value = 99999
            for next_move in moves:
                new_board = deepcopy(board)
                new_board.make_move(next_move, symbol)
                value = min(value, self.minmax(new_board, depth - 1, 'o'))
            return value
