import pygame
import pygame_menu
import constants
import time


class Interface:
    def __init__(self, game):
        self._game = game
        self._players = [None, None]  # classes of players (e.g. AIPlayerRandom, HumanPlayer, etc)

        self._tile_width = constants.window_width / game.board.width
        self._tile_height = constants.window_height / game.board.height

        self._symbols = {}  # dictionary in the form {'symbol': symbol_image}
        for symbol in constants.symbols + [None]:
            image = pygame.image.load(constants.symbols_images[symbol])
            image = pygame.transform.scale(image, (self._tile_width, self._tile_height))
            self._symbols[symbol] = image

        pygame.init()
        self._screen = pygame.display.set_mode((constants.window_width, constants.window_height))
        pygame.display.set_caption("Tic Tac Toe - Projekt SI - 184916 184306 184657")

        # Menu setup
        self._menu = pygame_menu.Menu("Tic Tac Toe", constants.window_width, constants.window_height,
                                      theme=pygame_menu.themes.THEME_DARK)

        player_selector_list = [('AlphaBeta AI', "AlphaBeta"),
                                ('MinMax AI', "MinMax"),
                                ('Random AI', "Random"),
                                ('Human', "Human")]
        self._menu.add.selector('Player 1: ', player_selector_list,
                                onchange=lambda _, player: self.set_player(0, constants.player_types[player]))
        self._menu.add.selector('Player 2: ', player_selector_list,
                                onchange=lambda _, player: self.set_player(1, constants.player_types[player]))
        self.set_player(0, constants.player_types[player_selector_list[0][1]])
        self.set_player(1, constants.player_types[player_selector_list[0][1]])

        self._menu.add.button('Play', self.play)
        self._menu.add.button('Quit', self._menu.disable)

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self._font = pygame.font.SysFont('Comic Sans MS', constants.display_font_size)

        self._clock = pygame.time.Clock()

    def display_menu(self):
        """enables and displays the menu"""
        self._menu.enable()
        self._menu.mainloop(self._screen)

    def display_result(self, winner):
        """displays the result of the game"""
        self._screen.fill(constants.white_color)
        if winner is None:
            text_surface = self._font.render(f"Draw!", False, (0, 0, 0))
        else:
            text_surface = self._font.render(f"Wins: {winner}.", False, (0, 0, 0))
        self._screen.blit(text_surface, (0, 0))
        pygame.display.update()
        pygame.display.flip()

        start = time.time()
        while time.time() - start < constants.results_displaying_time:
            pygame.event.get()

    def display_board(self, board):
        """displays the board on screen"""
        self._screen.fill(constants.white_color)
        for x in range(board.width):
            for y in range(board.height):
                self._screen.blit(self._symbols[board.get_tile((x, y))], (x * self._tile_width, y * self._tile_height))
        pygame.display.update()
        pygame.display.flip()

    def play(self):
        """runs the game"""
        self._game.set_players(self._players)
        self._game.play()

    def set_player(self, player_index, player_type):
        """sets type of player at player_index (0 or 1) to player_type (a class of the chosen player)"""
        self._players[player_index] = player_type

    def get_events(self):
        """returns game events: [event_type, mouse_x, mouse_y]"""  # is the event_type necessary? todo?
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                return constants.menu_exit, None, None
            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                return constants.mouse_clicked, int(mouse_pos[0]/self._tile_width), int(mouse_pos[1]/self._tile_height)

        self._clock.tick(30)
        pygame.display.update()
        pygame.display.flip()
        return None, None, None

    def __del__(self):
        pygame.quit()
