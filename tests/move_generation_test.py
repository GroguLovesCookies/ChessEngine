from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove
from typing import List


def generation_test(board, depth) -> int:
    if depth == 0:
        return 1

    generator = ChessMoveGenerator(board)
    moves: List[ChessMove] = generator.generate()
    positions: int = 0
    print(moves)

    for move in moves:
        move.make_move()
        positions += generation_test(board, depth-1)
        move.undo_move()

    return positions


parser = ChessParser()
board = parser.load("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")

print(generation_test(board, 2))