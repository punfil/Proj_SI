from human_player import HumanPlayer
from ai_player_random import AIPlayerRandom
from ai_player_minmax import AIPlayerMinMax
from ai_player_alphabeta import AIPlayerAlphaBeta
from ai_player_neat import AIPlayerNEAT
from ai_player_keras import AIPlayerKeras
from ai_player_neural import AIPlayerNeural

from neural_networks import FFNHyperparams

default_hyperparams = FFNHyperparams(num_inputs=25, num_outputs=1, hidden_dims=[25, 625, 625, 15625, 625, 625, 625, 25],
                                     activation_fcn='tanh', learning_rate=0.0001)
training_epochs = 75

menu_play_game = 0
menu_exit = 1
mouse_clicked = 0
results_displaying_time = 1
display_font_size = 30

ai_recursion_depth = 4
player_types = {
    "Human": HumanPlayer,
    "Random": AIPlayerRandom,
    "MinMax": AIPlayerMinMax,
    "AlphaBeta": AIPlayerAlphaBeta,
    "NEAT": AIPlayerNEAT,
    "Keras": AIPlayerKeras,
    "Neural": AIPlayerNeural
}

symbols = ['x', 'o']
symbols_images = {
    'x': "images/x.png",
    'o': "images/o.png",
    None: "images/empty.png"
}

board_width = 5
board_height = 5

window_height = 600
window_width = 600

white_color = (255, 255, 255)

required_line_length = 4  # how many symbols in a row are needed to win the game
