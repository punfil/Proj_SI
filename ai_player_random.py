from player import Player
import random


class AIPlayerRandom(Player):
    def __init__(self, symbol, game):
        super().__init__(symbol, game)

    def get_move(self):
        x, y = random.choice(self._game.board.get_free_tiles())
        return x, y

    def is_ready(self):
        return True
