from ai_player_alphabeta import AIPlayerAlphaBeta


class AIPlayerNEAT(AIPlayerAlphaBeta):
    def __init__(self, symbol, game, neural_network):
        super().__init__(symbol, game, 1, None)
        self._neural_network = neural_network

    def get_possible_moves(self, board):
        return board.get_free_tiles()

    def heuristic_function(self, board, active_player_symbol):
        return self._neural_network.activate(board.to_array(active_player_symbol))
