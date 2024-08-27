from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator

parser = ChessParser()
board = parser.load("8/1pP3p1/5p2/3p2P1/3P1P2/8/6Pp/8")

gen = ChessMoveGenerator(board)
print(gen.generate())
print(gen.generate(False))
