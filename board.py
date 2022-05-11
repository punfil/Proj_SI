class Board:
    def __init__(self, size):
        self._size = 3
        self._board = [[None for _ in range(size)] for _ in range(size)]

    def make_move(self, x, y, player):
        if x > self._size-1 or y > self._size-1 or y < 0 or x < 0:
            print("Entered wrong coordinates you moron\n")
            return False
        if self._board[x][y] is None:
            self._board[x][y] = player
            return True
        print("Entered occupied coordinates you idiot\n")
        return False

    def check_winning(self):
        # xxx
        for i in range(self._size):
            winning_inside = self._board[i][0]
            if winning_inside is None:
                continue
            for j in range(self._size):
                if self._board[i][j] != winning_inside:
                    break
                if j == self._size-1:
                    return winning_inside

        # przekatna - lewa dol prawa gorna
        winning_inside = self._board[0][self._size - 1]
        for i in range(self._size):
            if self._board[i][self._size-i-1] != winning_inside or winning_inside is None:
                break
            if i == self._size-1:
                return winning_inside

        # przekatna - lewa gora prawa dol
        winning_inside = self._board[0][0]
        for i in range(self._size):
            if self._board[i][i] != winning_inside or winning_inside is None:
                break
            if i == self._size-1:
                return winning_inside

        ### x
        ### x
        ### x
        for j in range(self._size):
            winning_inside = self._board[0][j]
            for i in range(self._size):
                if self._board[i][j] != winning_inside or winning_inside is None:
                    break
                if i == self._size-1:
                    return winning_inside
        return None

    def check_draw(self):
        for i in range(self._size):
            for j in range(self._size):
                if self._board[i][j] is None:
                    return False
        return True

    def check_free(self, x, y):
        return self._board[x][y] is None

    @property
    def size(self):
        return self._size

    def __getitem__(self, item):
        return self._board[item]