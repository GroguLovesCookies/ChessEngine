from typing import List
from pieces import chess_pieces


class Board:
    def __init__(self, generator, width=8, height=8):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.i = 0
        self.ep_square = [None, None]
        self.castling = [True, True, True, True]
        self.white = True
        self.pins = 0
        self.pin_rays = [0 for _ in range(8)]

        self.generator = generator(self)

        self.ep_stack = []
        self.castle_stack = []

        self.attacked_squares = set()
        self.pinned_pieces = {}

        self.kings = [(0, 0), (0, 0)]
        self.white_bitboards = {piece: 0 for piece in chess_pieces.values()}
        self.black_bitboards = {piece: 0 for piece in chess_pieces.values()}

    @property
    def white_bitboard(self):
        out = 0
        for bitboard in self.white_bitboards.values():
            out |= bitboard
        return out

    @property
    def black_bitboard(self):
        out = 0
        for bitboard in self.black_bitboards.values():
            out |= bitboard
        return out

    def get_bitboard(self, white):
        return self.white_bitboards if white else self.black_bitboards

    def orthogonal_bitboards(self, white):
        bitboards = self.get_bitboard(white)
        return bitboards[chess_pieces["q"]] | bitboards[chess_pieces["r"]]

    def diagonal_bitboards(self, white):
        bitboards = self.get_bitboard(white)
        return bitboards[chess_pieces["q"]] | bitboards[chess_pieces["b"]]

    def reload_attacked(self):
        ...# self.attacked_squares = set([i.end for i in self.generator.generate(not self.white, False, True)])

    def reload_pinned(self):
        offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        coords: tuple = self.kings[0 if self.white else 1]
        distances: List[int] = self.get_distances(coords)

        use_offsets = range(8)
        for i in use_offsets:
            offset = offsets[i]
            for t in range(1, distances[i]):
                target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)

    def reset_rights(self):
        self.ep_stack.append(self.ep_square)
        self.ep_square = [None, None]
        self.castle_stack.append(self.castling[:])
        self.white = not self.white

    def restore_rights(self):
        self.ep_square = self.ep_stack.pop(-1)
        self.castling = self.castle_stack.pop(-1)
        self.white = not self.white

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