from classes.board import Board
from pieces import is_white_piece


class Move:
    def __init__(self, board: Board, start: tuple, end: tuple):
        self.board = board
        self.start = start
        self.end = end
        self.piece_moved = board[start]
        self.piece_taken = board[end]
        self.is_white_move = is_white_piece(self.piece_moved)

    def make_move(self):
        ...

    def undo_move(self):
        ...

    def __repr__(self):
        ...