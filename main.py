from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator, calculate_pins, generate_attack_map
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces
from utils import print_bitboard

parser = ChessParser()
board = parser.load("r3k2r/pppppppp/8/8/8/8/PPPPPnPP/R111K2R")


print_bitboard(board.attacked_squares)
print(board.generator.generate(True))