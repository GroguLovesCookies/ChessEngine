import json
from typing import List, Dict

from classes.board import Board
from move_generators.chess_move_generator import generate_knight_moves, generate_king_moves
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from pieces import get_piece_value, chess_pieces, is_same_color
from utils import print_bitboard, square_to_index, index_to_square

offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
def create_sliding_mask(x: int, y: int, piece: str) -> bin:
    board = Board(MoveGenerator)
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

def generate_sliding_legal_moves(x, y, blockers, piece="r"):
    board = Board(MoveGenerator)
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
            if (blockers >> target_index) & 1 == 1:
                break

    return out

def create_sliding_lookup_table(piece="r"):
    rook_moves: Dict[int, Dict[bin, bin]] = {}
    for i in range(64):
        x = (63-i) % 8
        y = (63-i) // 8
        movement_mask = create_sliding_mask(x, y, piece)
        blocker_patterns = create_all_blocker_bitboards(movement_mask)
        cur_moves = {}
        for bitboard in blocker_patterns:
            legal_bitboard = generate_sliding_legal_moves(x, y, bitboard, piece)
            cur_moves[bitboard] = legal_bitboard
        rook_moves[i] = cur_moves

    return rook_moves

def create_knight_mask(x, y):
    out = 0
    for move in generate_knight_moves(Board(MoveGenerator),(x, y), False):
        out |= 1 << square_to_index(*move.end)
    return out

def create_king_mask(x, y):
    out = 0
    for move in generate_king_moves(Board(MoveGenerator),(x, y), False):
        out |= 1 << square_to_index(*move.end)
    return out

def generate_knight_legal_moves(x, y, blockers):
    return create_knight_mask(x, y) & ~blockers

def create_knight_lookup_table():
    knight_moves: Dict[int, Dict[bin, bin]] = {}
    for i in range(64):
        x = (63 - i) % 8
        y = (63 - i) // 8
        movement_mask = create_knight_mask(x, y)
        blocker_patterns = create_all_blocker_bitboards(movement_mask)
        cur_moves = {}
        for bitboard in blocker_patterns:
            legal_bitboard = generate_knight_legal_moves(x, y, bitboard)
            cur_moves[bitboard] = legal_bitboard
        knight_moves[i] = cur_moves

    return knight_moves

if __name__ == "__main__":
    with open("move_lookup.json", "r") as f:
        dictionary = json.loads(f.read())
    with open("move_lookup.json", "w") as f:
        f.close()
    with open("move_lookup.json", "r+") as f:
        f.truncate(0)
        dictionary["k"] = {"masks": {i: create_king_mask(*index_to_square(i)) for i in range(64)}}
        f.write(json.dumps(dictionary))