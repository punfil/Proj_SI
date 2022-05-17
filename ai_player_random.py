from player import Player
import random


class AIPlayerRandom(Player):
    def __init__(self, symbol, game):
        super().__init__(symbol, game)

    def return_random_move(self):
        return random.choice(self._game.board.get_free_tiles())

    def get_move(self):
        x, y = self.return_random_move()
        return x, y