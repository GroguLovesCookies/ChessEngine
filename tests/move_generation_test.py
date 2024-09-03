from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove
from typing import List

from utils import any_in_list


def generation_test(board, depth) -> int:
    if depth == 0:
        return 1

    generator = ChessMoveGenerator(board)
    moves: List[ChessMove] = generator.generate(board.white)
    positions: int = 0
    # print(moves)

    for move in moves:
        move.make_move()
        # print(move, end=" ")
        new = generation_test(board, depth-1)
        if depth == 1:
            print(move)
            print(new)
        positions += new
        move.undo_move()
        if depth == 3:
            break

    return positions


parser = ChessParser()
board = parser.load("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
board.castling[2] = False
board.castling[3] = False

# print(generation_test(board, 3))
moves = ChessMoveGenerator(board).generate(board.white)
moves[0].make_move()
moves = ChessMoveGenerator(board).generate(board.white)
move = any_in_list(moves, lambda x: repr(x) == "f2d3")
move.make_move()
print(moves[0])
print(parser.save(board))
print(generation_test(board, 1))