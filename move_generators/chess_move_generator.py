import json
from unicodedata import lookup

from classes.board import Board
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from pieces import chess_pieces, get_piece_value, is_white_piece, is_same_color, is_empty
from typing import List

from utils import print_bitboard, square_to_index, bitboard_to_moves

offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
def generate_sliding_moves(board: Board, coords: tuple, only_captures: bool, collide: bool = True) -> List[ChessMove]:
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
        moves_bitboard &= ~bitboard
        out |= moves_bitboard

    return bitboard_to_moves(out, coords, board, ChessMove)


def generate_knight_moves(board: Board, coords: tuple, _: bool) -> List[ChessMove]:
    lookup_table = board.generator.knight_lookup
    i = square_to_index(*coords)
    mask = lookup_table["masks"][str(i)]
    bitboard = mask & ~(board.white_bitboard if is_white_piece(board[coords]) else board.black_bitboard)
    return bitboard_to_moves(bitboard, coords, board, ChessMove)


def generate_king_moves(board: Board, coords: tuple, _: bool) -> List[ChessMove]:
    moves: List[ChessMove] = []
    distances: List[int] = board.get_distances(coords)

    use_offsets = range(8)

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, min(distances[i], 2)):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            if is_same_color(board[coords], board[target_coord]):
                break
            moves.append(ChessMove(board, coords, target_coord))

    rank: int = 7 if is_white_piece(board[coords]) else 0
    if coords != (4, rank):
        return moves

    if board.castling[0 if rank == 7 else 2]:
        if get_piece_value(board[(0, rank)]) == chess_pieces["r"] and \
            is_empty(board[(1, rank)]) and \
            is_empty(board[(2, rank)]) and \
            is_empty(board[(3, rank)]):
                moves.append(ChessMove(board, coords, (coords[0] + 1, coords[1]), ChessMove.MT_CASTLE_LONG))

    if board.castling[1 if rank == 7 else 3]:
        if get_piece_value(board[(7, rank)]) == chess_pieces["r"] and \
            is_empty(board[(6, rank)]) and \
            is_empty(board[(5, rank)]):
                moves.append(ChessMove(board, coords, (coords[0] + 1, coords[1]), ChessMove.MT_CASTLE_SHORT))

    return moves

def generate_pawn_moves(board: Board, coords: tuple, only_captures: bool) -> List[ChessMove]:
    moves: List[ChessMove] = []

    direction: int = -1 if is_white_piece(board[coords]) else 1
    distance_index: int = 2 if direction == 1 else 6
    distances: List[int] = board.get_distances(coords)
    distance: int = distances[distance_index]

    max_move_distance = 0 if only_captures else min(distance, 2 if distance < 7 else 3)
    for t in range(1, max_move_distance):
        target: tuple = (coords[0], coords[1] + direction * t)
        if board[target] != 0:
            break
        else:
            moves.append(ChessMove(board, coords, target, 0 if t == 1 else ChessMove.MT_DOUBLE_PUSH))

    if distance > 0:
        if distances[4] > 1:
            capture_target = (coords[0] - 1, coords[1] + direction)
            if (not is_same_color(board[coords], board[capture_target]) and board[capture_target] != 0) or only_captures:
                moves.append(ChessMove(board, coords, capture_target))
            if capture_target == board.ep_square[0]:
                moves.append(ChessMove(board, coords, capture_target, ChessMove.MT_EN_PASSANT))
        if distances[0] > 1:
            capture_target = (coords[0] + 1, coords[1] + direction)
            if (not is_same_color(board[coords], board[capture_target]) and board[capture_target] != 0) or only_captures:
                moves.append(ChessMove(board, coords, capture_target))
            if capture_target == board.ep_square[0]:
                moves.append(ChessMove(board, coords, capture_target, ChessMove.MT_EN_PASSANT))

    if distance == 2 and not only_captures:
        output = []
        for move in moves:
            output.append(ChessMove(board, coords, move.end, ChessMove.MT_PROMOTE_QUEEN))
            output.append(ChessMove(board, coords, move.end, ChessMove.MT_PROMOTE_ROOK))
            output.append(ChessMove(board, coords, move.end, ChessMove.MT_PROMOTE_BISHOP))
            output.append(ChessMove(board, coords, move.end, ChessMove.MT_PROMOTE_KNIGHT))
        return output

    return moves

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

    def filter_legal_moves(self, moves: List[ChessMove]) -> List[ChessMove]:
        filtered: List[ChessMove] = []
        for move in moves:
            if get_piece_value(move.piece_moved) == chess_pieces["k"]:
                if move.end not in self.board.attacked_squares:
                    filtered.append(move)
                continue
            filtered.append(move)
        return filtered

