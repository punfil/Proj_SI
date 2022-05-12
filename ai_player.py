from player import Player
from copy import deepcopy
from random import randint

class AIPlayer(Player):
    def __init__(self, level, sign, board):
        self._level = level
        self._change_level = level
        super().__init__(sign, board)

    def return_random_move(self):
        while True:
            x, y = randint(0, self._board.width - 1), randint(0, self._board.height - 1)
            if self._board.check_free((x, y)):
                return x, y

    def get_move(self, mouse_x, mouse_y):
        if self._change_level == 1:  # Easy - always random
            if self._level == 2:
                self._change_level = 2
            x, y = self.return_random_move()
            return x, y

        elif self._change_level == 2 or self._level == 3:  # Hard - always AI, Medium - once hard once easy
            if self._level == 2:
                self._change_level = 1
            opponents_sign = 'x'
            # Try to win in current turn
            for i in range(0, self._board._size):
                for j in range(0, self._board._size):
                    if self._board.check_free(i, j):
                        copy = deepcopy(self._board)
                        copy.make_move(i, j, self._sign)
                        if copy.check_winning() == self._sign:
                            return i, j

            # Check if player can win somewhere - block him!
            for i in range(0, self._board._size):
                for j in range(0, self._board._size):
                    if self._board.check_free(i, j):
                        copy = deepcopy(self._board)
                        copy.make_move(i, j, opponents_sign)
                        if copy.check_winning() == opponents_sign:
                            return i, j

            # Try to take center
            if self._board.check_free(1, 1):
                return 1, 1
            # Try to take corners
            if self._board.check_free(0, 2):
                return 0, 2
            elif self._board.check_free(0, 0):
                return 0, 0
            elif self._board.check_free(2, 0):
                return 2, 0
            elif self._board.check_free(2, 2):
                return 2, 2
            x, y = self.return_random_move()
            return x, y

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, new_level):
        self._level = new_level
        self._change_level = new_level
