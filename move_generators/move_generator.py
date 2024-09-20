from classes.board import Board
from typing import List, Dict, Callable

from moves.move import Move
from pieces import is_white_piece, get_piece_value


class MoveGenerator:
    generators: Dict[int, Callable[[Board, tuple, bool], List[Move]]] = {}
    def __init__(self, board: Board):
        self.board = board

    def generate(self, white:bool = True, do_filter:bool=True, only_captures:bool=False) -> List[Move]:
        self.pre_generate()
        moves: List[Move] = []
        y: int = 0
        for row in self.board:
            x: int = 0
            for piece in row:
                if piece == 0:
                    x += 1
                    continue
                if get_piece_value(piece) in self.generators.keys() and is_white_piece(piece) == white:
                    moves.extend(self.generators[get_piece_value(piece)](self.board, (x, y), only_captures))
                x += 1
            y += 1
        return moves if not self.board.checked else self.filter_legal_moves(moves)

    def pre_generate(self):
        ...

    def filter_legal_moves(self, moves: List[Move]) -> List[Move]:
        ...

    def filter_piece_moves(self, coords, bitboard):
        ...