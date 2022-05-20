class Player:
    def __init__(self, symbol, game):
        self._symbol = symbol
        self._game = game

    def get_move(self):
        raise NotImplementedError()
    
    def is_ready(self):
        raise NotImplementedError()

    @property
    def symbol(self):
        return self._symbol
