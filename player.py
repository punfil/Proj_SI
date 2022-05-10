class Player:
    def __init__(self, sign, board):
        self._sign = sign
        self._board = board

    def get_move(self):
        a = input("Input coordinates in format x,y\n")
        try:
            coords = a.split(',')
            x, y = int(coords[0]), int(coords[1])
        except:
            print("Entered wrong coordinates format you donkey")
            x, y = -1, -1
        finally:
            return x, y

    def make_move(self, x, y):
        self._board.make_move(x, y, self._sign)

    @property
    def sign(self):
        return self._sign
