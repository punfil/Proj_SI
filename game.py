from fast_board import FastBoard
from interface import Interface
from ai_player import AIPlayer
from ai_player_neat import AIPlayerNEAT
from ai_player_keras import AIPlayerKeras
from model import TicTacToeModel
import heuristics
import constants
import time
import copy
import numpy as np
import random
from random import randrange
import neat
import pickle
import numpy as np
import matplotlib.pyplot as plt


class Game:
    def __init__(self, board_width=constants.board_width, board_height=constants.board_height):
        self._board = FastBoard(board_width, board_height)

        self._players = []

        self._interface = Interface(self)

        self._click_x = None
        self._click_y = None

        self._trainingHistory = []
        self._ticTacToeModel = TicTacToeModel(constants.board_height*constants.board_width, 3, 100, 32)

    def menu(self):
        """displays the menu"""
        self._interface.display_menu()

    def set_players(self, player_types):
        """sets the player list to players of the types (classes) given in player_types"""
        self._players = []
        for index, player_type in enumerate(player_types):
            symbol = constants.symbols[index]
            if issubclass(player_type, AIPlayerNEAT):
                with open("best.pickle", "rb") as file:
                    genome = pickle.load(file)
                config_path = "./config.txt"
                config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                            neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                net = neat.nn.FeedForwardNetwork.create(genome, config)

                player = AIPlayerNEAT(symbol, self, net)
            elif issubclass(player_type, AIPlayer):
                player = player_type(symbol, self,
                                     constants.ai_recursion_depth, heuristics.better_line_length)
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

    def play(self, display_interface=True, clear_board=True):
        """plays a single game. Returns (winner's symbol, number of turns the game took, game duration)"""

        if clear_board:
            self._board.clear()

        # current_player_index = random.randint(0, 1)
        current_player_index = 0
        start_time = time.time()
        winner = None
        turns = 0

        game_running = True

        while game_running:
            turns += 1

            if display_interface:
                self._interface.display_board(self._board)
                print(f"move: {turns}")

            current_player = self._players[current_player_index]
            current_player_index = (current_player_index + 1) % len(self._players)

            # repeat until player makes a valid move (for human players accidentaly clicking occupied tiles)
            try_again = True
            while try_again:
                try:
                    self._click_x = None
                    self._click_y = None
                    self._interface.get_events()  # without this line the window freezes in long AI vs AI games
                    while not current_player.is_ready():
                        event_type, mouse_x, mouse_y = self._interface.get_events()
                        if event_type == constants.menu_exit:
                            game_running = False
                        elif event_type == constants.mouse_clicked:
                            self._click_x = mouse_x
                            self._click_y = mouse_y
                    if not game_running:
                        break

                    x, y = current_player.get_move()
                    self._board.make_move((x, y), current_player.symbol)
                    try_again = False
                except ValueError:
                    print("Wrong move!")


            winner = self._board.get_winner()
            if winner or self._board.check_draw():
                self._interface.display_board(self._board)
                game_running = False
                if display_interface:
                    print("winner:", winner)
                    print("game lasted", time.time()-start_time, "\n")
                    self._interface.display_result(winner)

        return winner, turns, time.time() - start_time

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

    def generate_single(self):
        """Generate single game
        AlphaBeta - 60% moves
        Random - 40% moves"""
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
            choose_players = randrange(10) + 1  # od 1-4 grają randomy, od 5 do 10 gra Alpha
            if choose_players <= 4:
                self.set_players([constants.player_types["Random"], constants.player_types["Random"]])
            else:
                self.set_players([constants.player_types["AlphaBeta"], constants.player_types["AlphaBeta"]])

            # self._interface.display_board(self._board)
            # time.sleep(2)
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
                if winner == 'x':
                    result = -1
                elif winner == 'o':
                    result = 1
                else:
                    result = 0
        for historyItem in boardHistory:
            self._trainingHistory.append((result, copy.deepcopy(historyItem)))

    def generate_data(self, n, postfix=""):
        """Generate n games and save to file with postfix"""
        for i in range(n):
            self.generate_single()
            if i % (n / 100) == 0:
                print(i, "/", n, " - ", (i * 100) // n, "%")
        self.save_data(postfix)

    def save_data(self, postfix=""):
        """save data from training History"""
        with open('./data/data_%i_size_%s.pickle' % (constants.board_width, postfix), 'wb') as f:
            pickle.dump(self._trainingHistory, f)

    def load_data(self, postfix=""):
        """load data to training History"""
        loaded = []
        with open('./data/data_%i_size_%s.pickle' % (constants.board_width, postfix), 'rb') as f:
            loaded = pickle.load(f)
        for l in loaded:
            self._trainingHistory.append(l)

    def save_model(self):
        """save model (previous is overwritten!!!)"""
        self._ticTacToeModel.save()

    def load_model(self):
        """Load last saved model"""
        self._ticTacToeModel.load()

    def load_best_model(self):
        """Load best model"""
        self._ticTacToeModel.load_best()

    def save_best_model(self):
        """Load best model"""
        self._ticTacToeModel.save_best()

    def train_start(self):
        """Train keras model, generate or load data and train"""
        #self.generate_data(10000, "RandomAlphax10000_5x5_3")
        self.load_data("RandomAlphax10000_5x5")
        self.load_data("RandomAlphax10000_5x5_2")
        #self.load_data("RandomAlphax10000_5x5_3")
        self._ticTacToeModel.train(self._trainingHistory)

    def generate_statistic(self):
        """Generate bar statistic for n games (Statistic for players choosen in menu)"""
        n = 100
        statistic = {'x': 0, 'o': 0, 'draw': 0}


        for _ in range(n):
            symbol, turns, dur = self.play(False,True)
            if symbol == 'x':
                statistic['x'] = statistic.get('x', 0) + 1
            elif symbol == 'o':
                statistic['o'] = statistic.get('o', 0) + 1
            else:
                statistic['draw'] = statistic.get('draw', 0) + 1

        courses = list(statistic.keys())
        values = list(statistic.values())
        plt.bar(courses, values, color='maroon', width=0.4)
        plt.xlabel("Wyniki gier")
        plt.ylabel("Ilość danego wyniku")
        plt.title("Statystyki %i gier"%n)
        plt.show()
    def generate_training_data(self, num_games=50):
        """generates training data for Neural Heuristics AI.
        The data is a json file containing: {"board_representation": eval, ...}
        """

        with open("board_evaluations.json", 'w') as file:
            # creating and clearing the file that the results will be saved into
            file.write("{\n")  # opening json bracket

        for i in range(num_games):

            self._players = [None, None]
            self._players[0] = constants.player_types["AlphaBeta"]('x', self, constants.ai_recursion_depth,
                                                                   heuristics.better_line_length, save_evaluations=True)
            self._players[1] = constants.player_types["AlphaBeta"]('o', self, constants.ai_recursion_depth,
                                                                   heuristics.better_line_length, save_evaluations=True)
            self._board.clear()
            for j in range(random.choice((0, 2, 2, 2, 4, 4, 6, 6))):
                # each player makes a few random moves before the start of the real game
                # this is to increase variation in the training data and reduce the chance of evaluating same boards

                if j % 2 == 0:
                    symbol = 'x'
                else:
                    symbol = 'o'

                tiles = self._board.get_free_tiles()
                self._board.make_move(random.choice(tiles), symbol)

            self.play(display_interface=True, clear_board=False)

        with open("board_evaluations.json", 'a') as file:
            file.write("}")  # closing json bracket

    def eval_genomes(self, initial_genomes, config):
        """for every genome in initial_genomes, plays the game with NN created from that genome against a random AI
        Assigns fitness scores depending on results and length of the game.
        """
        nets = []
        genomes = []
        players = []

        for genome_id, genome in initial_genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            player = constants.player_types["NEAT"]('x', self, net)
            players.append(player)
            genomes.append(genome)

        self._players = [None, None]
        num_games = 2  # how many games a single player plays before being assigned a final fitness

        for i, player in enumerate(players):
            for j in range(num_games):
                self._players[0] = player
                self._players[1] = constants.player_types["Random"]('o', self)

                winner, turns, game_time = self.play(display_interface=False)

                if winner:
                    if winner == player.symbol:
                        genomes[i].fitness += 100 - turns
                    else:
                        genomes[i].fitness += -100 + turns

                print(f"game {i}-{j} finished")
                print("winner:", winner)
                print("game lasted", game_time)
                print(f"fitness: {genomes[i].fitness}\n")

            genomes[i].fitness /= num_games
            print(f"final fitness: {genomes[i].fitness}\n\n")

    def neat_train_start(self):
        """trains the NEAT AI. When finished, saves the best genome to a file named 'best.pickle'"""
        config_path = "./config.txt"
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
        population = neat.Population(config)
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)

        winner = population.run(self.eval_genomes, 50)
        pickle.dump(winner, open("best.pickle", "wb"))

    @property
    def board(self):
        return self._board

    @property
    def click_position(self):
        return self._click_x, self._click_y

    @property
    def model(self):
        return self._ticTacToeModel
