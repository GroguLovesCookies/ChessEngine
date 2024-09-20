from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator, calculate_pins, generate_attack_map
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces
from utils import print_bitboard

parser = ChessParser()
board = parser.load("rnbqkbnr/1ppppppp/8/1P1R4/4B3/1p6/P7/K6r")


print_bitboard(board.attacked_squares)
print(board.generator.generate(True))