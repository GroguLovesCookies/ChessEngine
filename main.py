from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove
from moves.move import Move
from pieces import chess_pieces
from utils import print_bitboard

parser = ChessParser()
board = parser.load("rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
board.castling[2] = False
board.castling[3] = False

moves = board.generator.generate()
print(moves)


# ChessMove(board, (1, 0), (5, 0)).make_move()
moves[0].make_move()
moves[0].undo_move()
print()
print_bitboard(board.white_bitboards[chess_pieces["p"]])
print()
print_bitboard(board.white_bitboards[chess_pieces["q"]])