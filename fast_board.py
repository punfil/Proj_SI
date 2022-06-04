import constants
from board import Board


class FastBoard(Board):
    """same as normal Board, but stores some information instead of recalculating everything every time"""
    def __init__(self, width, height):
        super().__init__(width, height)
        self._winner = None
        self._free_tiles = {(x, y) for x in range(self._width) for y in range(self._height)}
        self._free_tiles_with_neighbour = set()
        self._occupied_tiles = set()

    def make_move(self, position, player_symbol):
        super().make_move(position, player_symbol)
        self.update_winner(position)
        self._occupied_tiles.add(position)
        self._free_tiles.discard(position)
        self._free_tiles_with_neighbour.discard(position)
        if len(self._free_tiles) != len(self._free_tiles_with_neighbour):
            for x_offset in (-1, 0, 1):
                for y_offset in (-1, 0, 1):
                    if (position[0] + x_offset, position[1] + y_offset) in self._free_tiles:
                        self._free_tiles_with_neighbour.add((position[0] + x_offset, position[1] + y_offset))

    def clear(self):
        super().clear()
        self._winner = None
        self._free_tiles = {(x, y) for x in range(self._width) for y in range(self._height)}
        self._free_tiles_with_neighbour = set()
        self._occupied_tiles = set()

    def get_free_tiles(self):
        return list(self._free_tiles)

    def get_free_tiles_with_neighbour(self):
        return list(self._free_tiles_with_neighbour)

    def get_occupied_tiles(self):
        return list(self._occupied_tiles)

    def update_winner(self, position):
        """updates the self._winner variable if the provided position is part of the winning line"""
        # todo remove code repetitions
        # --- horizontal ---
        line_length = 0
        current_symbol = None
        y = position[1]
        for x in range(self._width):
            tile = self.get_tile((x, y))
            if tile is not None:
                if tile != current_symbol:
                    current_symbol = tile
                    line_length = 1
                else:
                    line_length += 1

                if line_length >= constants.required_line_length:
                    # print("---HORIZONTAL VICTORY---", current_symbol)
                    self._winner = current_symbol
                    return

        # ||| vertical |||
        line_length = 0
        current_symbol = None
        x = position[0]
        for y in range(self._height):
            tile = self.get_tile((x, y))
            if tile is not None:
                if tile != current_symbol:
                    current_symbol = tile
                    line_length = 1
                else:
                    line_length += 1

                if line_length >= constants.required_line_length:
                    # print("\\\\\\DIAGONAL VICTORY\\\\\\", current_symbol)
                    self._winner = current_symbol
                    return

        # diagonals adapted from this:
        # https://stackoverflow.com/questions/56815012/how-to-get-the-element-which-are-diagonal-to-a-certain-index-in-an-array-which-r

        # /// diagonal ///
        line_length = 0
        current_symbol = None
        x = position[0] + min(self._width - position[0] - 1, position[1])
        y = position[1] - min(self._width - position[0] - 1, position[1])
        while x >= 0 and y < self._height:
            tile = self.get_tile((x, y))
            if tile is not None:
                if tile != current_symbol:
                    current_symbol = tile
                    line_length = 1
                else:
                    line_length += 1

                if line_length >= constants.required_line_length:
                    # print("///DIAGONAL VICTORY///", current_symbol)
                    self._winner = current_symbol
                    return
            x -= 1
            y += 1

        # \\\ diagonal \\\
        line_length = 0
        current_symbol = None
        x = position[0] - min(position[0], position[1])
        y = position[1] - min(position[0], position[1])
        while x < self._width and y < self._height:
            tile = self.get_tile((x, y))
            if tile is not None:
                if tile != current_symbol:
                    current_symbol = tile
                    line_length = 1
                else:
                    line_length += 1

                if line_length >= constants.required_line_length:
                    # print("|||VERTICAL VICTORY|||", current_symbol)
                    self._winner = current_symbol
                    return
            x += 1
            y += 1

    def get_winner(self):
        return self._winner
