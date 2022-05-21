import constants


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

    def get_winner(self):
        """checks if there is a winning player on a given board. If no board was given, uses the current game board.
        Returns the winner's symbol, or None if there is no winner
        """

        # --- horizontal ---
        for y in range(self._height):
            line_length = 0
            current_symbol = None
            for x in range(self._width):
                if self.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        # print("---HORIZONTAL VICTORY---", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self.get_tile((x, y))

        # ||| vertical |||
        for x in range(self._width):
            line_length = 0
            current_symbol = None
            for y in range(self._height):
                if self.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        # print("|||VERTICAL VICTORY|||", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self.get_tile((x, y))

        # /// diagonal ///
        for diagonal in range(self._width + self._height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < self._width else diagonal - self._width + 1
            end_x = diagonal if diagonal < self._height else self._height - 1
            for x in range(start_x, end_x + 1):
                y = diagonal - x
                if self.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        # print("///DIAGONAL VICTORY///", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self.get_tile((x, y))

        # \\\ diagonal \\\
        for diagonal in range(self._width + self._height):
            line_length = 0
            current_symbol = None

            start_x = 0 if diagonal < self._width else diagonal - self._width + 1
            end_x = diagonal if diagonal < self._height else self._height - 1
            for x in range(start_x, end_x + 1):
                y = self._height - (diagonal - x) - 1
                if self.get_tile((x, y)) == current_symbol:
                    line_length += 1
                    if line_length >= constants.required_line_length and current_symbol is not None:
                        # print("\\\\\\DIAGONAL VICTORY\\\\\\", current_symbol)
                        return current_symbol
                else:
                    line_length = 1
                    current_symbol = self.get_tile((x, y))

        return None

    def check_draw(self):
        """returns True if there are no available moves and there is no winner and False otherwise"""
        if not self.get_free_tiles():
            if self.get_winner() is not None:
                return True
        return False

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
