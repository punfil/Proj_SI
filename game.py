from player import Player
from ai_player import AIPlayer
from board import Board
from display_component import DisplayComponent
import constants
import time


class Game:
    def __init__(self, board_width=constants.board_width, board_height=constants.board_height, difficulty=3):
        self._board = Board(board_width, board_height)

        self._players = [Player('x', self._board),
                         AIPlayer(difficulty, 'o', self._board)]
        self._current_player = constants.starting_player

        self._display_component = DisplayComponent()
        self._exit = False

    def restart(self):
        """restarts the game"""
        self._board.clear()
        self._current_player = constants.starting_player

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

    def check_winning(self):

        # --- horizontal ---
        for y in range(self._board.height):
            line_length = 0
            current_symbol = None
            for x in range(self._board.width):
                if self._board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("---HORIZONTAL VICTORY---")
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self._board.get_tile((x, y))

        # ||| vertical |||
        for x in range(self._board.width):
            line_length = 0
            current_symbol = None
            for y in range(self._board.height):
                if self._board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("|||VERTICAL VICTORY|||")
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self._board.get_tile((x, y))

        # /// diagonal ///
        for diagonal in range(self._board.width + self._board.height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < self._board.width else diagonal - self._board.width + 1
            end_x = diagonal if diagonal < self._board.height else self._board.height - 1
            for x in range(start_x, end_x+1):
                y = diagonal - x
                if self._board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("///DIAGONAL VICTORY///")
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self._board.get_tile((x, y))

        # \\\ diagonal \\\
        for diagonal in range(self._board.width + self._board.height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < self._board.width else diagonal - self._board.width + 1
            end_x = diagonal if diagonal < self._board.height else self._board.height - 1
            for x in range(start_x, end_x + 1):
                y = self._board.height - (diagonal - x) - 1
                if self._board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("\\\\\\DIAGONAL VICTORY\\\\\\")
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self._board.get_tile((x, y))

        return None

    def check_draw(self):
        for x in range(self._board.width):
            for y in range(self._board.height):
                if self._board.get_tile((x, y)) is None:
                    return False
        return True

    def play(self):
        self.deal_with_menu()

        while not self._exit:
            current_game_winner = None
            quit = False

            # For displaying results
            game_finished = False
            time_start_displaying_result = None

            # For displaying screen before game - prolog
            game_started = False
            time_start_game_after_prolog = time.time()

            while not quit:
                if not game_finished and game_started:
                    self._display_component.display_board(self._board)
                elif game_finished:
                    self._display_component.display_result(current_game_winner)
                    if time.time()-time_start_displaying_result > constants.results_displaying_time:
                        quit = True
                elif not game_started:
                    self._display_component.display_prolog(self._players[0].sign)
                    if time.time()-time_start_game_after_prolog > constants.prolog_displaying_time:
                        game_started = True

                event_type, x, y = self._display_component.get_events()
                if event_type == constants.menu_exit:
                    self._exit = True
                    quit = True
                    break
                elif (event_type == constants.mouse_clicked or self._current_player == 'o') and not game_finished and game_started: #If it's players turn and he made the decision or it's ai's turn
                    current_player = self.return_player_with_sign(self._current_player)  # pycharm says this doesn't return anything, todo
                    x, y = current_player.get_move(x, y)
                    current_player.make_move((x, y))
                    possible_winner = self.check_winning()
                    if possible_winner is not None or self.check_draw():
                        current_game_winner = possible_winner
                        game_finished = True
                        time_start_displaying_result = time.time()
                    self.change_current_player()

            if not self._exit:
                self._display_component.display_result(constants.results_draw if current_game_winner is None else current_game_winner)
                self.restart()
                self.deal_with_menu()
