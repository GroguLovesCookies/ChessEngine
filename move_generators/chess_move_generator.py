from classes.board import Board
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from pieces import chess_pieces, get_piece_value, get_piece_color
from typing import List


offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
def generate_sliding_moves(board: Board, coords: tuple) -> List[ChessMove]:
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
            if get_piece_color(board[coords]) == get_piece_color(piece_at_coord):
                break
            moves.append(ChessMove(board, coords, target_coord))
            if piece_at_coord != 0:
                break

    return moves


def generate_knight_moves(board: Board, coords: tuple) -> List[ChessMove]:
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
        if board[end] == 0 or get_piece_color(board[end]) != get_piece_color(board[coords]):
            moves.append(ChessMove(board, coords, end))

        if offset[0] != 0:
            if distances[2] >= 2:
                end = (branch_coord[0], branch_coord[1] + 1)
        else:
            if distances[0] >= 2:
                end = (branch_coord[0] + 1, branch_coord[1])
        if board[end] == 0 or get_piece_color(board[end]) != get_piece_color(board[coords]):
            moves.append(ChessMove(board, coords, end))
    return moves


def generate_king_moves(board: Board, coords: tuple) -> List[ChessMove]:
    moves: List[ChessMove] = []
    distances: List[int] = board.get_distances(coords)

    use_offsets = range(8)

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, min(distances[i], 2)):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            if get_piece_color(board[coords]) == get_piece_color(board[target_coord]):
                break
            moves.append(ChessMove(board, coords, target_coord))

    return moves

def generate_pawn_moves(board: Board, coords: tuple) -> List[ChessMove]:
    return []

class ChessMoveGenerator(MoveGenerator):
    generators = {
        chess_pieces["r"]: generate_sliding_moves,
        chess_pieces["b"]: generate_sliding_moves,
        chess_pieces["q"]: generate_sliding_moves,
        chess_pieces["n"]: generate_knight_moves,
        chess_pieces["k"]: generate_king_moves,
        chess_pieces["p"]: generate_pawn_moves
    }


