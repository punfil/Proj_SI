from fast_board import FastBoard
from interface import Interface
from ai_player import AIPlayer
from ai_player_neat import AIPlayerNEAT
from ai_player_keras import AIPlayerKERAS
from model import TicTacToeModel
import heuristics
import constants
import time
import copy
import numpy as np
import random
#import neat
import pickle


class Game:
    def __init__(self, board_width=constants.board_width, board_height=constants.board_height):
        self._board = FastBoard(board_width, board_height)

        self._players = []

        self._interface = Interface(self)

        self._click_x = None
        self._click_y = None

        self._trainingHistory = []
        self._ticTacToeModel = TicTacToeModel(9, 3, 100, 32)
    def menu(self):
        """displays the menu"""
        self._interface.display_menu()

    def set_players(self, player_types):
        """sets the player list to players of the types (classes) given in player_types"""
        self._players = []
        for index, player_type in enumerate(player_types):
            symbol = constants.symbols[index]
            # if issubclass(player_type, AIPlayerNEAT):
            #     with open("best.pickle", "rb") as file:
            #         genome = pickle.load(file)
            #     config_path = "./config.txt"
            #     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
            #                                 neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
            #     net = neat.nn.FeedForwardNetwork.create(genome, config)

            if issubclass(player_type, AIPlayer):
                player = player_type(symbol, self,
                                     constants.ai_recursion_depth, heuristics.line_length_turn_number)
            else:
                player = player_type(symbol, self)
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

    def get_logic_board(self):
        """Create board with int values on slots
            x = 1
            o = -1
            None = 0 """
        b = copy.deepcopy(self._board.board)
        logic_board = []
        for list in b:
            row = []
            for el in list:
                if el == None:
                    row.append(0)
                elif el == 'x':
                    row.append(1)
                else:
                    row.append(-1)
            logic_board.append(row)
        return logic_board

    def symulate(self, n):
        """symulate n games and append trainig data to trainingHistory"""
        for i in range(n):
            boardHistory = []
            result = 0
            self._board.clear()

            # current_player_index = random.randint(0, 1)
            current_player_index = 0
            game_running = True
            start_time = time.time()
            move_num = 0
            while game_running:
                move_num += 1
                # if move_num == 2:
                #     self.set_players([constants.player_types["Random"], constants.player_types["Random"]])
                # if move_num == 4:
                #     self.set_players([constants.player_types["AlphaBeta"], constants.player_types["AlphaBeta"]])

               # self._interface.display_board(self._board)
                #time.sleep(2)
                current_player = self._players[current_player_index]
                current_player_index = (current_player_index + 1) % len(self._players)

                self._click_x = None
                self._click_y = None
                self._interface.get_events()  # without this line the window freezes in long AI vs AI games
                while not current_player.is_ready():
                    event_type, mouse_x, mouse_y = self._interface.get_events()
                    if event_type == constants.menu_exit:
                        game_running = False
                        break
                    elif event_type == constants.mouse_clicked:
                        self._click_x = mouse_x
                        self._click_y = mouse_y

                x, y = current_player.get_move()
                self._board.make_move((x, y), current_player.symbol)
                boardHistory.append(self.get_logic_board())

                winner = self._board.get_winner()
                if winner or self._board.check_draw():
                    game_running = False
                    print("winner:", winner,"  ",i , "/", n )
                    #print("game lasted", time.time() - start_time, "\n")
                    if winner == 'x':
                        result = -1
                    elif winner == 'o':
                        result = 1
                    else:
                        result = 0
                    #self._interface.display_result(winner)
            for historyItem in boardHistory:
                self._trainingHistory.append((result, copy.deepcopy(historyItem)))

    def save_data(self, postfix = ""):
        """save data from training History"""
        with open('./data/data_%i_size_%s.pickle'%(constants.board_width,postfix), 'wb') as f:
            pickle.dump(self._trainingHistory, f)
    def load_data(self, postfix = ""):
        """load data to training History"""
        with open('./data/data_%i_size_%s.pickle'%(constants.board_width,postfix), 'rb') as f:
            self._trainingHistory = pickle.load(f)

    def save_model(self):
        """save model (previous is overwritten!!!)"""
        self._ticTacToeModel.save()
    def load_model(self):
        """Load last saved model"""
        self._ticTacToeModel.load()
    def load_bigdata_model(self):
        """Load model learned on bigdata.pickle"""
        self._ticTacToeModel.load_bigdata()

    def train_start(self):
        #1. Trenowanie na nowych danych
        #self.set_players([constants.player_types["Random"],constants.player_types["Random"]]) #wybrac jakich graczy chcemy
        #self.symulate(liczba) #wybrac liczbe gier
        #self._ticTacToeModel.train(self._trainingHistory)
        #self.save_data(nazwa_prefixu) #zapisac wygenerowane dane pod unikalny plik
        #2. Trenowanie z pliku
        #self.load_data(nazwa)
        #self._ticTacToeModel.train(self._trainingHistory)
        self.set_players([constants.player_types["AlphaBeta"], constants.player_types["AlphaBeta"]])
        self.symulate(1000) #wybrac liczbe gier
        self._ticTacToeModel.train(self._trainingHistory)
        self.save_data("MieszanieRandomzAlphax1000") #zapisac wygenerowane dane pod unikalny plik


    @property
    def board(self):
        return self._board

    @property
    def click_position(self):
        return self._click_x, self._click_y

    @property
    def model(self):
        return self._ticTacToeModel