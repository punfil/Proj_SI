from player import Player
from ai_player import AIPlayer
from board import Board
from display_component import DisplayComponent
import constants
import time


class Game:
    def __init__(self, board_width=constants.board_width, board_height=constants.board_height):
        self._board = Board(board_width, board_height)

        self._players = [Player('x', self), AIPlayer('o', self, 2)]
        self._current_player = constants.starting_player

        self._display_component = DisplayComponent(self)
        self._exit = False

        self._mouse_x = None
        self._mouse_y = None

    def restart(self):
        """restarts the game"""
        self._board.clear()
        self._current_player = constants.starting_player

    def change_current_player(self):
        if self._current_player == 'x':
            self._current_player = 'o'
        else:
            self._current_player = 'x'

    def return_player_with_symbol(self, symbol):
        if self._players[0].symbol == symbol:
            return self._players[0]
        return self._players[1]

    def check_winning(self, board=None):

        if board is None:
            board = self._board

        # --- horizontal ---
        for y in range(board.height):
            line_length = 0
            current_symbol = None
            for x in range(board.width):
                if board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("---HORIZONTAL VICTORY---", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = board.get_tile((x, y))

        # ||| vertical |||
        for x in range(board.width):
            line_length = 0
            current_symbol = None
            for y in range(board.height):
                if board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("|||VERTICAL VICTORY|||", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = board.get_tile((x, y))

        # /// diagonal ///
        for diagonal in range(board.width + board.height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < board.width else diagonal - board.width + 1
            end_x = diagonal if diagonal < board.height else board.height - 1
            for x in range(start_x, end_x+1):
                y = diagonal - x
                if board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("///DIAGONAL VICTORY///", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = board.get_tile((x, y))

        # \\\ diagonal \\\
        for diagonal in range(board.width + board.height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < board.width else diagonal - board.width + 1
            end_x = diagonal if diagonal < board.height else board.height - 1
            for x in range(start_x, end_x + 1):
                y = board.height - (diagonal - x) - 1
                if board.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        print("\\\\\\DIAGONAL VICTORY\\\\\\", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = board.get_tile((x, y))

        return None

    def check_draw(self, board=None):
        if board is None:
            board = self._board

        for x in range(board.width):
            for y in range(board.height):
                if board.get_tile((x, y)) is None:
                    return False
        return True

    def play(self):
        while not self._exit:
            current_game_winner = None
            stop = False

            # For displaying results
            game_finished = False
            time_start_displaying_result = None

            # For displaying screen before game - prolog
            game_started = False
            time_start_game_after_prolog = time.time()

            while not stop:
                if not game_finished and game_started:
                    self._display_component.display_board(self._board)
                elif game_finished:
                    self._display_component.display_result(current_game_winner)
                    if time.time()-time_start_displaying_result > constants.results_displaying_time:
                        stop = True
                elif not game_started:
                    self._display_component.display_prolog(self._players[0].symbol)
                    if time.time()-time_start_game_after_prolog > constants.prolog_displaying_time:
                        game_started = True

                event_type, self._mouse_x, self._mouse_y = self._display_component.get_events()
                if event_type == constants.menu_exit:
                    self._exit = True
                    stop = True
                    break
                elif (event_type == constants.mouse_clicked or self._current_player == 'o') and not game_finished and game_started: #If it's players turn and he made the decision or it's ai's turn
                    current_player = self.return_player_with_symbol(self._current_player)  # pycharm says this doesn't return anything, todo
                    print("game getting move")
                    x, y = current_player.get_move()
                    print("game making move")
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

    @property
    def board(self):
        return self._board

    @property
    def mouse_position(self):
        return self._mouse_x, self._mouse_y
