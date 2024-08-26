class Board:
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.i = 0

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