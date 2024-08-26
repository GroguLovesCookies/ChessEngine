from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("R7/8/8/3q4/8/8/8/8")

gen = ChessMoveGenerator(board)