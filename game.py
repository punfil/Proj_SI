from player import Player
from ai_player import AIPlayer
from board import Board
from display_component import DisplayComponent
import constants


class Game:
    def __init__(self, board_size=3, diff=3):
        self._board_size = board_size
        self._board = Board(board_size)

        self._players = [None for _ in range(constants.players_count)]
        self._players[0] = Player('x', self._board)
        self._players[1] = AIPlayer(diff, 'o', self._board)
        self._current_player = constants.starting_player

        self._display_component = DisplayComponent()
        self._exit = False

    def clear_board(self):
        self._board = Board(self._board_size)
        for player in self._players:
            player.board = self._board

    def update_ai_player_difficulty(self, new_difficulty):
        self._players[1].level = new_difficulty

    def change_current_player(self):
        if self._current_player == 'x':
            self._current_player = 'o'
        else:
            self._current_player = 'x'

    def return_player_with_sign(self, sign):
        if self._players[0].sign == sign:
            return self._players[0]
        return self._players[1]

    def deal_with_menu(self):
        activity, variable1 = self._display_component.use_menu()
        if activity == constants.menu_play_game:
            self.update_ai_player_difficulty(variable1)
        elif activity == constants.menu_exit:
            self._exit = constants.menu_exit
        elif activity == constants.menu_instruction:
            self._display_component.display_instruction()
            return self.deal_with_menu()

    def play(self):
        self.deal_with_menu()
        while not self._exit:
            current_game_winner = None
            quit = False
            while not quit:
                self._display_component.display_board(self._board)
                event_type, x, y = self._display_component.get_events()
                if event_type == constants.menu_exit:
                    self._exit = True
                    quit = True
                    break
                elif event_type == constants.mouse_clicked:
                    for i in range(2):
                        current_player = self.return_player_with_sign(self._current_player)
                        x, y = current_player.get_move(x, y)
                        current_player.make_move(x, y)
                        possible_winner = self._board.check_winning()
                        if possible_winner is not None:
                            current_game_winner = possible_winner
                            quit = True
                            break
                        self.change_current_player()
            self._display_component.display_result(constants.results_draw if current_game_winner is None else current_game_winner)
            self.clear_board()
            self.deal_with_menu()
