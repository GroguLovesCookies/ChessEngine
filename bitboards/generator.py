import json
from typing import List, Dict

from classes.board import Board
from move_generators.chess_move_generator import ChessMoveGenerator, offsets
from moves.chess_move import ChessMove
from pieces import get_piece_value, chess_pieces, is_same_color
from utils import print_bitboard


def create_sliding_mask(x: int, y: int, piece: str) -> bin:
    board = Board(ChessMoveGenerator)
    coords = (x, y)
    distances: List[int] = board.get_distances(coords)
    out: bin = 0

    use_offsets = range(8)
    if piece == "r":
        use_offsets = [0, 2, 4, 6]
    elif piece == "b":
        use_offsets = [1, 3, 5, 7]

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, distances[i]):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            target_index: int = target_coord[0] + target_coord[1] * 8
            target_index = 63 - target_index
            out |= 1 << target_index


    return out


def create_all_blocker_bitboards(movement_mask: bin):
    square_indices: List[int] = []
    for i in range(64):
        if (movement_mask >> i) & 1 == 1:
            square_indices.append(i)

    num_patterns: int = 1 << len(square_indices)
    blocker_bitboards: List[bin] = [0 for _ in range(num_patterns)]
    for i in range(num_patterns):
        for j in range(len(square_indices)):
            bit: int = (i >> j) & 1
            blocker_bitboards[i] |= bit << square_indices[j]

    return blocker_bitboards

def generate_rook_legal_moves(x, y, blockers):
    board = Board(ChessMoveGenerator)
    coords = (x, y)
    distances: List[int] = board.get_distances(coords)
    out: bin = 0

    use_offsets = [0, 2, 4, 6]

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, distances[i]):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            target_index: int = target_coord[0] + target_coord[1] * 8
            target_index = 63 - target_index
            out |= 1 << target_index
            if (blockers >> target_index) & 1 == 1:
                break

    return out

def create_rook_lookup_table():
    rook_moves: Dict[int, Dict[bin, bin]] = {}
    for i in range(64):
        x = (63-i) % 8
        y = (63-i) // 8
        movement_mask = create_sliding_mask(x, y, "r")
        blocker_patterns = create_all_blocker_bitboards(movement_mask)
        cur_moves = {}
        for bitboard in blocker_patterns:
            legal_bitboard = generate_rook_legal_moves(x, y, bitboard)
            cur_moves[bitboard] = legal_bitboard
        rook_moves[i] = cur_moves

    return rook_moves

moves = create_rook_lookup_table()
print_bitboard(moves[0][6])
with open("move_lookup.json", "w") as f:
    f.write(json.dumps({"r": {"masks": {i: create_sliding_mask((63-i) % 8, (63-i)//8, "r") for i in range(64)}, "moves": moves}}))