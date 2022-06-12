from ai_player_alphabeta import AIPlayerAlphaBeta
import numpy as np
from neural_networks import build_model
import constants


class AIPlayerNeural(AIPlayerAlphaBeta):
    def __init__(self, symbol, game, recursion_depth, heuristic_function, save_evaluations=False):
        super().__init__(symbol, game, recursion_depth=1, heuristic_function=None, save_evaluations=save_evaluations)

        hp = constants.default_hyperparams
        model = build_model(hp)
        model.load_weights('./training/model_best_weights')

        self._model = model

    def heuristic_function(self, board, active_player_symbol):
        winner = board.get_winner()
        if winner:
            if winner == active_player_symbol:
                return 1
            else:
                return -1
        input_data = np.array([board.to_array(active_player_symbol)])
        return self._model.predict(input_data)[0][0]
