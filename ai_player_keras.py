from keras.layers import Dense
from keras.layers import Dropout
from keras.models import Sequential
from keras.utils import to_categorical
import numpy as np
from player import Player
import copy
import random


class AIPlayerKERAS(Player):

    def get_possible_moves(self, board):
        moves = board.get_free_tiles_with_neighbour()
        if not moves:
            moves = board.get_free_tiles()
        return moves

    # def get_move(self):
    #     availableMoves = self.get_possible_moves(self._game.board)
    #     val_list = []
    #     val_list2 = []
    #     val_list1 = []
    #     maxValue = 0
    #     bestMove = availableMoves[0]
    #     for availableMove in availableMoves:
    #         # get a copy of a board
    #         value = 0
    #         value2 = 0
    #         value1 = 0
    #         boardCopy = copy.deepcopy(self._game.get_logic_board())
    #         print("Wolne pole: " , boardCopy[availableMove[0]][availableMove[1]])
    #         if self._symbol == 'x':
    #             boardCopy[availableMove[0]][availableMove[1]] = -1
    #             value = self._game.model.predict(boardCopy, 0)
    #             value2 = self._game.model.predict(boardCopy, 2)
    #             value1 = self._game.model.predict(boardCopy, 1)
    #         else:
    #             boardCopy[availableMove[0]][availableMove[1]] = 1
    #             value = self._game.model.predict(boardCopy, 2)
    #         if value > maxValue:
    #             maxValue = value
    #             bestMove = availableMove
    #         val_list.append(value)
    #         val_list2.append(value2)
    #         val_list1.append(value1)
    #         print("x: " ,value, " ", availableMove)
    #         print("o: " ,value2, " ", availableMove)
    #         print("draw: ", value1, " ", availableMove)
    #
    #     print(val_list)
    #     print(val_list2)
    #     print(val_list1)
    #     print("best: ", bestMove)
    #     print("best val: ", maxValue)
    #     return bestMove

    def get_move(self):
        availableMoves = self.get_possible_moves(self._game.board)
        val_list = []
        val_list2 = []
        val_list1 = []
        minValue = 1.0
        bestMove = availableMoves[0]
        for availableMove in availableMoves:
            # get a copy of a board
            value = 1.0
            value2 = 1.0
            value1 = 1.0
            boardCopy = copy.deepcopy(self._game.get_logic_board())
            #print("Wolne pole: " , boardCopy[availableMove[0]][availableMove[1]])
            if self._symbol == 'x':
                boardCopy[availableMove[0]][availableMove[1]] = -1
                value = self._game.model.predict(boardCopy, 2)
                value2 = self._game.model.predict(boardCopy, 0)
                value1 = self._game.model.predict(boardCopy, 1)
            else:
                boardCopy[availableMove[0]][availableMove[1]] = 1
                value = self._game.model.predict(boardCopy, 0)
                value2 = self._game.model.predict(boardCopy, 2)
                value1 = self._game.model.predict(boardCopy, 1)
            if value <= minValue:
                minValue = value
                bestMove = availableMove
            val_list.append((value,availableMove))
            val_list2.append((value2,availableMove))
            val_list1.append((value1,availableMove))

        print("enemy: ",val_list)
        print("me: ",val_list2)
        print("draw: ",val_list1)
        print("best: ", bestMove)
        print("best val: ", minValue)
        return bestMove

    def is_ready(self):
        return True