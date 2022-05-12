class Board:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._board = [[None for y in range(height)] for x in range(width)]

    def get_tile(self, position):
        """returns tile at given position"""

        if position[0] > self._width-1 or position[1] > self._height-1 or position[0] < 0 or position[1] < 0:
            raise ValueError(f"Position {position} is outside of board")

        return self._board[position[0]][position[1]]

    def clear(self):
        """clears the board"""
        for x in range(self._width):
            for y in range(self._height):
                self._board[x][y] = None

    def make_move(self, position, player_symbol):
        """places player symbol at specified position, if it was free and within the board bounds"""

        x = position[0]
        y = position[1]
        if x > self._width-1 or y > self._height-1 or y < 0 or x < 0:
            raise ValueError(f"Position {position} is outside of board")

        if self._board[x][y] is None:
            self._board[x][y] = player_symbol
        else:
            raise ValueError(f"Position {position} is not empty")

    def check_free(self, position):
        """checks if the given position is occupied"""
        return self.get_tile(position) is None

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __getitem__(self, item):
        return self._board[item]
