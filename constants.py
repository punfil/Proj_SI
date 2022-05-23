from human_player import HumanPlayer
from ai_player_random import AIPlayerRandom
from ai_player_minmax import AIPlayerMinMax
from ai_player_alphabeta import AIPlayerAlphaBeta
from ai_player_neat import AIPlayerNEAT

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
    "NEAT": AIPlayerNEAT
}

symbols = ['x', 'o']
symbols_images = {
    'x': "images/x.png",
    'o': "images/o.png",
    None: "images/empty.png"
}

board_width = 8
board_height = 8

window_height = 800
window_width = 800

white_color = (255, 255, 255)

required_line_length = 5  # how many symbols in a row are needed to win the game
