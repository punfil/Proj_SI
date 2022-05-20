from player import Player


class HumanPlayer(Player):
    def get_move(self):
        return self._game.click_position
    
    def is_ready(self):
        click_pos = self._game.click_position
        if click_pos[0] is None or click_pos[1] is None:
            return False
        return True
