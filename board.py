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

    def get_free_tiles(self):
        """returns a list of all unoccupied tiles"""
        free_tiles = []
        for x in range(self._width):
            for y in range(self._height):
                if self._board[x][y] is None:
                    free_tiles.append((x, y))
        return free_tiles

    def get_free_tiles_with_neighbour(self):
        """returns a list of all unoccupied tiles that have an occupied neighbour tile"""
        # todo I don't think this gives any faster results than normal get_tiles
        output = []
        for x, y in self.get_free_tiles():
            stop = False
            for x_offset in (-1, 0, 1):
                if stop:
                    break
                for y_offset in (-1, 0, 1):
                    if stop:
                        break
                    try:
                        if not self.check_free((x+x_offset, y+y_offset)):
                            output.append((x, y))
                            stop = True
                    except ValueError:
                        pass

        return output

    def check_free(self, position):
        """checks if the given position is occupied"""
        return self.get_tile(position) is None

    def iter_lines(self, line_length):
        """returns all lines (diagonal, vertical, horizontal) of given length"""

        # horizontal
        for n_row in range(self.height):
            for start_column in range(self.width - line_length+1):
                yield self._board[n_row][start_column:start_column + line_length]

        # vertical
        for n_column in range(self.width):
            for start_row in range(self.height - line_length+1):
                yield [self._board[n_row][n_column] for n_row in range(start_row, start_row + line_length)]

        # diagonal
        for n_row in range(self.height - line_length+1):
            for n_column in range(self.width - line_length+1):
                yield [self._board[n_row + i][n_column + i] for i in range(line_length)]  # decreasing
                yield [self._board[n_row + i][self.width - 1 - n_column - i] for i in range(line_length)]  # increasing

    def draw(self):  # todo delete this, only for temporary debugging
        for y in range(self._height):
            for x in range(self._width):
                print(self._board[x][y] if self._board[x][y] is not None else '.', end='')
            print()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def __getitem__(self, item):
        return self._board[item]
