from fast_board import FastBoard
from interface import Interface
from ai_player import AIPlayer
import heuristics
import constants
import time
import random


class Game:
    def __init__(self, board_width=constants.board_width, board_height=constants.board_height):
        self._board = FastBoard(board_width, board_height)

        self._players = []

        self._interface = Interface(self)

        self._click_x = None
        self._click_y = None

    def menu(self):
        """displays the menu"""
        self._interface.display_menu()

    def set_players(self, player_types):
        """sets the player list to players of the types (classes) given in player_types"""
        self._players = []
        for index, player_type in enumerate(player_types):
            if issubclass(player_type, AIPlayer):
                player = player_type(constants.symbols[index], self,
                                     constants.ai_recursion_depth, heuristics.line_length_turn_number)
            else:
                player = player_type(constants.symbols[index], self)
            self._players.append(player)

    def get_next_symbol(self, current_symbol):
        """returns the symbol of the next player, assuming the current player's symbol is current_symbol"""
        index = constants.symbols.index(current_symbol)
        return constants.symbols[(index + 1) % len(constants.symbols)]

    def get_previous_symbol(self, current_symbol):
        """returns the symbol of the previous player, assuming the current player's symbol is current_symbol"""
        index = constants.symbols.index(current_symbol)
        return constants.symbols[(index - 1) % len(constants.symbols)]

    def play(self):
        """runs the game"""
        self._board.clear()

        # current_player_index = random.randint(0, 1)
        current_player_index = 0
        game_running = True
        start_time = time.time()

        while game_running:
            self._interface.display_board(self._board)

            current_player = self._players[current_player_index]
            current_player_index = (current_player_index + 1) % len(self._players)

            self._click_x = None
            self._click_y = None
            self._interface.get_events()  # without this line the window freezes in long AI vs AI games
            while not current_player.is_ready():
                event_type, mouse_x,  mouse_y = self._interface.get_events()
                if event_type == constants.menu_exit:
                    game_running = False
                    break
                elif event_type == constants.mouse_clicked:
                    self._click_x = mouse_x
                    self._click_y = mouse_y

            x, y = current_player.get_move()
            self._board.make_move((x, y), current_player.symbol)

            winner = self._board.get_winner()
            if winner or self._board.check_draw():
                game_running = False
                print("winner:", winner)
                print("game lasted", time.time()-start_time, "\n")
                self._interface.display_result(winner)

    @property
    def board(self):
        return self._board

    @property
    def click_position(self):
        return self._click_x, self._click_y
