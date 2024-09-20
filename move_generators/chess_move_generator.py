import json

from classes.board import Board
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from pieces import chess_pieces, get_piece_value, is_white_piece, is_same_color, is_empty, is_diagonal_piece, \
    is_orthogonal_piece
from typing import List

from utils import print_bitboard, square_to_index, bitboard_to_moves, bitboard_to_pawn_moves, any_in_list, \
    index_to_square

offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
ks_castle = 0b00000110
qs_castle = 0b01110000
castle_king = 0b00001000
ks_castle_rook = 0b00000001
qs_castle_rook = 0b10000000

def generate_sliding_map(board: Board, coords: tuple):
    out = 0
    pieces = []
    if get_piece_value(board[coords]) in [chess_pieces["r"], chess_pieces["q"]]:
        pieces.append(chess_pieces["r"])
    if get_piece_value(board[coords]) in [chess_pieces["b"], chess_pieces["q"]]:
        pieces.append(chess_pieces["b"])
    for piece in pieces:
        lookup_table = board.generator.rook_lookup if piece == chess_pieces["r"] else board.generator.bishop_lookup
        i = square_to_index(*coords)
        mask = lookup_table["masks"][str(i)]
        blockers = board.white_bitboard | board.black_bitboard
        blockers &= mask
        bitboard = board.white_bitboard if is_white_piece(board[coords]) else board.black_bitboard
        moves_bitboard = lookup_table["moves"][str(i)][str(blockers)]
        out |= moves_bitboard
    return out

def generate_piece_map(board: Board, coords: tuple, lookup: dict):
    i = square_to_index(*coords)
    mask = lookup["masks"][str(i)]
    return mask

def generate_sliding_moves(board: Board, coords: tuple, only_captures: bool, collide: bool = True) -> List[ChessMove]:
    out = generate_sliding_map(board, coords)
    bitboard = board.white_bitboard if is_white_piece(board[coords]) else board.black_bitboard
    out &= ~bitboard
    out = filter_piece_moves(board, coords, out)
    return bitboard_to_moves(out, coords, board, ChessMove)


def generate_knight_moves(board: Board, coords: tuple, _: bool) -> List[ChessMove]:
    mask  = generate_piece_map(board, coords, board.generator.knight_lookup)
    bitboard = mask & ~(board.white_bitboard if is_white_piece(board[coords]) else board.black_bitboard)
    return bitboard_to_moves(bitboard, coords, board, ChessMove)


def generate_king_moves(board: Board, coords: tuple, _: bool) -> List[ChessMove]:
    mask = generate_piece_map(board, coords, board.generator.king_lookup)
    white = is_white_piece(board[coords])
    colour_bitboard = board.white_bitboard if white else board.black_bitboard
    bitboard = mask & ~colour_bitboard
    bitboard &= ~board.attacked_squares

    moves = bitboard_to_moves(bitboard, coords, board, ChessMove)
    if board.checked:
        return moves

    offset = 0 if white else 56
    blockers = board.attacked_squares | colour_bitboard
    if board.castling[0 if white else 2]:
        ks_castle_mask = ks_castle << offset
        ks_castle_rook_mask = ks_castle_rook << offset

        if blockers & ks_castle_mask == 0 and ks_castle_rook_mask & board.get_bitboard(white)[chess_pieces["r"]] > 0:
            moves.append(ChessMove(board, coords, index_to_square(square_to_index(*coords) - 2), ChessMove.MT_CASTLE_SHORT))
    if board.castling[1 if white else 3]:
        qs_castle_mask = qs_castle << offset
        qs_castle_rook_mask = qs_castle_rook << offset

        if blockers & qs_castle_mask == 0 and qs_castle_rook_mask & board.get_bitboard(white)[chess_pieces["r"]] > 0:
            moves.append(ChessMove(board, coords, index_to_square(square_to_index(*coords) + 2), ChessMove.MT_CASTLE_LONG))



    return moves

def generate_pawn_moves(board: Board, coords: tuple, only_captures: bool) -> List[ChessMove]:
    direction: int = -1 if is_white_piece(board[coords]) else 1
    distance_index: int = 2 if direction == 1 else 6
    distances: List[int] = board.get_distances(coords)
    distance: int = distances[distance_index]

    bitboard = 0

    max_move_distance = 0 if only_captures else min(distance, 2 if distance < 7 else 3)
    for t in range(1, max_move_distance):
        target: tuple = (coords[0], coords[1] + direction * t)
        if board[target] != 0:
            break
        else:
            bitboard |= 1 << square_to_index(*target)

    if distance > 0:
        if distances[4] > 1:
            capture_target = (coords[0] - 1, coords[1] + direction)
            if (not is_same_color(board[coords], board[capture_target]) and board[capture_target] != 0) or only_captures:
                bitboard |= 1 << square_to_index(*capture_target)
            if capture_target == board.ep_square[0]:
                bitboard |= 1 << square_to_index(*capture_target)
        if distances[0] > 1:
            capture_target = (coords[0] + 1, coords[1] + direction)
            if (not is_same_color(board[coords], board[capture_target]) and board[capture_target] != 0) or only_captures:
                bitboard |= 1 << square_to_index(*capture_target)
            if capture_target == board.ep_square[0]:
                bitboard |= 1 << square_to_index(*capture_target)

    if only_captures:
        return bitboard

    bitboard = filter_piece_moves(board, coords, bitboard)
    return bitboard_to_pawn_moves(bitboard, coords, board, ChessMove, is_white_piece(board[coords]))

def calculate_pins(board: Board, white: bool):
    king_coords = board.kings[0 if white else 1]
    enemy_bitboards = board.black_bitboards if white else board.white_bitboards

    board.pins = 0
    board.pin_rays = []

    use_offsets = []
    distances = board.get_distances(king_coords)
    if enemy_bitboards[chess_pieces["q"]] > 0:
        use_offsets = range(8)
    else:
        if enemy_bitboards[chess_pieces["r"]] > 0:
            use_offsets.extend([0, 2, 4, 6])
        if enemy_bitboards[chess_pieces["b"]] > 0:
            use_offsets.extend([1, 3, 5, 7])

    for i in use_offsets:
        offset = offsets[i]
        diagonal = i % 2 == 1

        lookup = board.generator.bishop_lookup if diagonal else board.generator.rook_lookup
        slider_bitboards = board.diagonal_bitboards(not white) if diagonal else board.orthogonal_bitboards(not white)
        king_ray_mask = lookup["masks"][str(square_to_index(*king_coords))]

        if king_ray_mask & slider_bitboards == 0:
            continue

        distance = distances[i]
        has_friendly_piece = False
        ray_mask = 0
        board.pin_rays.append(0)

        for t in range(1, distance):
            target_square = (king_coords[0] + t * offset[0], king_coords[1] + t * offset[1])
            ray_mask |= 1 << square_to_index(*target_square)
            piece = board[target_square]

            if not is_empty(piece):
                if is_white_piece(piece) == white:
                    if not has_friendly_piece:
                        has_friendly_piece = True
                    else:
                        break
                else:
                    piece_type = get_piece_value(piece)
                    if (diagonal and is_diagonal_piece(piece_type)) or (not diagonal and is_orthogonal_piece(piece_type)):
                        if has_friendly_piece:
                            board.pins |= ray_mask
                            board.pin_rays[-1] |= ray_mask
                        else:
                            board.double_check = board.checked
                            board.checked = True
                        break
                    else:
                        break


def filter_piece_moves(board, coords, bitboard):
    if is_pinned(board, *coords):
        pin = find_pin_index(board, *coords)
        print(pin)
        if pin != 0:
            return bitboard & pin
    return bitboard

def generate_attack_map(board: Board, white: bool):
    out = 0
    y: int = 0
    for row in board:
        x: int = 0
        for piece in row:
            if piece == 0 or is_white_piece(piece) != white:
                x += 1
                continue
            if get_piece_value(piece) in [chess_pieces["r"], chess_pieces["b"], chess_pieces["q"]]:
                out |= generate_sliding_map(board, (x, y))
            elif get_piece_value(piece) == chess_pieces["n"]:
                out |= generate_piece_map(board, (x, y), board.generator.knight_lookup)
            elif get_piece_value(piece) == chess_pieces["k"]:
                out |= generate_piece_map(board, (x, y), board.generator.king_lookup)
            else:
                out |= generate_pawn_moves(board, (x, y), True)
            x += 1
        y += 1
    return out

def is_pinned(board, x, y):
    return (board.pins >> square_to_index(x, y)) & 1 != 0

def find_pin_index(board, x, y):
    for i, pin in enumerate(board.pin_rays):
        if (pin >> square_to_index(x, y)) & 1 != 0:
            return pin
    return -1

class ChessMoveGenerator(MoveGenerator):
    generators = {
        chess_pieces["r"]: generate_sliding_moves,
        chess_pieces["b"]: generate_sliding_moves,
        chess_pieces["q"]: generate_sliding_moves,
        chess_pieces["n"]: generate_knight_moves,
        chess_pieces["k"]: generate_king_moves,
        chess_pieces["p"]: generate_pawn_moves
    }

    def __init__(self, board):
        super().__init__(board)
        with open("bitboards/move_lookup.json", "r") as f:
            moves = json.loads(f.read())
            self.rook_lookup = moves["r"]
            self.bishop_lookup = moves["b"]
            self.knight_lookup = moves["n"]
            self.king_lookup = moves["k"]

    def pre_generate(self):
        calculate_pins(self.board, self.board.white)

    def filter_legal_moves(self, moves: List[ChessMove]) -> List[ChessMove]:
        filtered: List[ChessMove] = []
        for move in moves:
            move.make_move()
            responses = generate_attack_map(self.board, self.board.white)
            king_bitboard = self.board.get_bitboard(not self.board.white)[chess_pieces["k"]]
            if responses & king_bitboard == 0:
                filtered.append(move)
            move.undo_move()

        return filtered