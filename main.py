from fen_parsers.chess_parser import ChessParser
from move_generators.chess_move_generator import ChessMoveGenerator
from moves.chess_move import ChessMove

parser = ChessParser()
board = parser.load("rbnq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R")
board.castling[2] = False
board.castling[3] = False

gen = ChessMoveGenerator(board)
moves = gen.generate(True)
print(moves)