class Player:
    def __init__(self, sign, board):
        self._sign = sign
        self._board = board

    def get_move(self, mouse_x, mouse_y):
            return mouse_x, mouse_y

    def make_move(self, x, y):
        self._board.make_move(x, y, self._sign)

    @property
    def sign(self):
        return self._sign

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_board):
        self._board = new_board
