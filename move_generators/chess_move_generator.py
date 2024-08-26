from classes.board import Board
from move_generators.move_generator import MoveGenerator
from moves.chess_move import ChessMove
from pieces import chess_pieces
from typing import List


def generate_sliding_moves(board: Board, coords: tuple) -> List[ChessMove]:
    moves: List[ChessMove] = []
    offsets = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
    distances = [
        board.width - coords[0],
        min(board.width - coords[0], board.height - coords[1]),
        board.height - coords[1],
        min(coords[0], board.height - coords[1]),
        coords[0],
        min(coords[0], coords[1]),
        coords[1],
        min(board.width - coords[0], coords[1])
    ]

    use_offsets = range(8)
    if board[coords] == chess_pieces["r"]:
        use_offsets = [0, 2, 4, 6]
    elif board[coords] == chess_pieces["b"]:
        use_offsets = [1, 3, 5, 7]

    for i in use_offsets:
        offset = offsets[i]
        for t in range(1, distances[i]):
            target_coord: tuple = (coords[0] + offset[0] * t, coords[1] + offset[1] * t)
            moves.append(ChessMove(board, coords, target_coord))

    return moves


def generate_knight_moves(board: Board, coords: tuple) -> List[ChessMove]:
    return []

def generate_king_moves(board: Board, coords: tuple) -> List[ChessMove]:
    return []

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


