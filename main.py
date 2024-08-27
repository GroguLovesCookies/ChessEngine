from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator

parser = ChessParser()
board = parser.load("8/8/3p4/8/4N3/21311/8/8")

gen = ChessMoveGenerator(board)
print(gen.generate())
