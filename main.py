from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator, calculate_pins
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces
from utils import print_bitboard

parser = ChessParser()
board = parser.load("3n4/1K2P2r/8/8/413/8/8/71")

board.castling[2] = False
board.castling[3] = False


moves = board.generator.generate()
print(moves)