from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("4k2r/8/8/8/7R/71/7K/8")

gen = ChessMoveGenerator(board)
moves = gen.generate(True)
print(moves)