from classes.board import Board
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces, get_piece_value, get_piece_color, is_white_piece, is_same_color, is_empty
from typing import List

from utils import any_in_list

offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
def generate_sliding_moves(board: Board, coords: tuple, only_captures: bool) -> List[ChessMove]:
    moves: List[ChessMove] = []
    distances: List[int] = board.get_distances(coords)

    use_offsets = range(8)
    if get_piece_value(board[coords]) == chess_pieces["r"]:
        use_offsets = [0, 2, 4, 6]
    elif get_piece_value(board[coords]) == chess_pieces["b"]:
        use_offsets = [1, 3, 5, 7]

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, distances[i]):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            piece_at_coord: int = board[target_coord]
            if is_same_color(board[coords], piece_at_coord) or (piece_at_coord != 0 and only_captures):
                break
            moves.append(ChessMove(board, coords, target_coord))
            if piece_at_coord != 0:
                break

    return moves


def generate_knight_moves(board: Board, coords: tuple, _: bool) -> List[ChessMove]:
    moves: List[ChessMove] =  []
    distances: List[int] = board.get_distances(coords)
    for i in [0, 2, 4, 6]:
        if distances[i] < 3:
            continue
        offset = offsets[i]
        branch_coord = (coords[0] + offset[0] * 2, coords[1] + offset[1] * 2)
        end = None
        if offset[0] != 0:
            if distances[6] >= 2:
                end = (branch_coord[0], branch_coord[1] - 1)
        else:
            if distances[4] >= 2:
                end = (branch_coord[0] - 1, branch_coord[1])
        if end is not None and not is_same_color(board[end], board[coords]):
            moves.append(ChessMove(board, coords, end))

        end = None
        if offset[0] != 0:
            if distances[2] >= 2:
                end = (branch_coord[0], branch_coord[1] + 1)
        else:
            if distances[0] >= 2:
                end = (branch_coord[0] + 1, branch_coord[1])
        if end is not None and not is_same_color(board[end], board[coords]):
            moves.append(ChessMove(board, coords, end))
    return moves


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

    def filter_legal_moves(self, moves: List[ChessMove]) -> List[ChessMove]:
        filtered: List[ChessMove] = []
        for move in moves:
            if get_piece_value(move.piece_moved) == chess_pieces["k"]:
                if move.end not in self.board.attacked_squares:
                    filtered.append(move)
                continue

        return filtered

