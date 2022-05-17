class Player:
    def __init__(self, symbol, game):
        self._symbol = symbol
        self._game = game

    def get_move(self):
        return self._game.mouse_position

    def make_move(self, position):
        self._game.board.make_move(position, self._symbol)

    @property
    def symbol(self):
        return self._symbol
