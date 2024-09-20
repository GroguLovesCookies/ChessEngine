from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator, calculate_pins
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces
from utils import print_bitboard

parser = ChessParser()
board = parser.load("rnbqkbnr/1ppppppp/8/1P6/8/1p6/P7/K7")


moves = board.generator.generate(True)
print(parser.save(board))
moves = board.generator.generate()
print(moves)
