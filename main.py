from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator

parser = ChessParser()
board = parser.load("8/8/1N6/3r4/8/8/8/8")

gen = ChessMoveGenerator(board)
print(gen.generate())
