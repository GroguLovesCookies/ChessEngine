class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.i = 0
        self.ep_square = None
        self.castling = [True, True, True, True]

        self.ep_stack = []
        self.castle_stack = []

    def reset_rights(self):
        self.ep_stack.append(self.ep_square)
        self.ep_square = None
        self.castle_stack.append(self.castling[:])

    def restore_rights(self):
        self.ep_square = self.ep_stack.pop(-1)
        self.castling = self.castle_stack.pop(-1)

    def __getitem__(self, item):
        if type(item) == int:
            return self.board[item]
        elif type(item) == tuple:
            return self.board[item[1]][item[0]]

    def __setitem__(self, key, value):
        if type(key) == tuple:
            self.board[key[1]][key[0]] = value

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        self.i += 1
        if self.i > self.height:
            raise StopIteration
        return self[self.i-1]

    def get_distances(self, coords):
        return [
            self.width - coords[0],
            min(self.width - coords[0], self.height - coords[1]),
            self.height - coords[1],
            min(coords[0] + 1, self.height - coords[1]),
            coords[0] + 1,
            min(coords[0] + 1, coords[1] + 1),
            coords[1] + 1,
            min(self.width - coords[0], coords[1] + 1)
        ]